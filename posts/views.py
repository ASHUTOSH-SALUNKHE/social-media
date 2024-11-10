from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Like, Post , UserProfile
from . import forms
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from django.http import JsonResponse
from .models import Post, Comment
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from .models import Follow
# Create your views here.
@login_required
@login_required
def newpost_list(request):
    # Fetch posts in descending order by date
    posts = Post.objects.select_related('author').order_by('-date')
    userprofiles = UserProfile.objects.all()  # Get all user profiles
    return render(request, 'newpost_page.html', {
        'posts': posts,
        'userprofiles': userprofiles,
    })


@login_required
def userpost_list(request, slug):
    # Use get_object_or_404 to handle non-existent posts gracefully
    post = Post.objects.get(slug=slug)
    return render(request, 'userpost_page.html', {'posts': post})


@login_required(login_url="/authme/login/")  # Ensure the user is logged in to add a post
def add_post(request):
    if request.method == 'POST': 
        form = forms.createPost(request.POST, request.FILES) 
        if form.is_valid():
            newpost = form.save(commit=False) 
            newpost.author = request.user 
            newpost.save() # Add success message
            return redirect('posts:newpost')  # Redirect to the new post list or specific post
    else:
        form = forms.createPost()
    return render(request, 'addpost_page.html', {'form': form})


#extracting all usernames in the explore user section
@login_required
def exp_users(request):
    # Retrieve all users and their profile pictures
    userprofile = UserProfile.objects.all()
    return render(request, 'explore_users.html', {'userprofile': userprofile})


#for uploading profile pic 
@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Filter to get posts by the logged-in user
    posts = Post.objects.filter(author=request.user).order_by('-date')  # Fetch only the user's posts
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('posts:profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile.html', {
        'form': form,
        'user_profile': user_profile,
        'posts': posts  # Pass only the user's posts
    })


@login_required
def delete_profile_picture(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.profile_picture:
        user_profile.profile_picture.delete()  # Delete the existing profile picture file
        user_profile.profile_picture = './default_profile.png'  # Reset to default profile picture
        user_profile.save()
    return redirect('posts:profile')



#to see specific user all posts
@login_required
def user_posts(request, username, profile_picture_url=None):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Handle profile_picture_url if needed
    return render(request, 'user_posts.html', {
        'user': user, 
        'posts': posts,
        'user_profile': user_profile,
    })

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            # If the like already exists, this means the user has liked it before
            like.delete()  # Remove like (unlike feature)
            action = 'unliked'
        else:
            # Like was created, meaning the user liked it for the first time
            action = 'liked'

        # Return the new like count as a JSON response
        return JsonResponse({'likes_count': post.likes.count(), 'action': action})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            comment = Comment.objects.create(post=post, user=request.user, text=comment_text)
            # Prepare the response data
            response_data = {
                'comment_id': comment.id,
                'username': comment.user.username,
                'text': comment.text,
            }
            return JsonResponse(response_data)  # Return a JSON response with the new comment data

    return JsonResponse({'error': 'Invalid comment'}, status=400)



#@require_http_methods(["DELETE"])
@require_POST  # Ensure it handles only POST requests
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return JsonResponse({'success': True})

def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', user_id=user_id)

def toggle_follow(request, username):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, username=username)
        user_profile = user_to_follow.userprofile
        
        if request.user in user_profile.followers.all():
            user_profile.followers.remove(request.user)
            is_following = False
        else:
            user_profile.followers.add(request.user)
            is_following = True

        return JsonResponse({'is_following': is_following})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_post(request, post_id):
    print(f"Trying to delete post with ID: {post_id} by user: {request.user}")
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect('posts:profile')