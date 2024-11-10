from django.contrib import admin
from django.urls import include, path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.newpost_list, name='newpost'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),  # Ensure this is correct
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
     path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('addpost/', views.add_post, name='addpost'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('toggle_follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('exp_users/', views.exp_users, name='exp_users'),
    path('profile/', views.profile, name='profile'),
    path('profile/delete/', views.delete_profile_picture, name='delete_profile_picture'),
    path('posts/<slug:slug>/', views.userpost_list, name='userpost'),
    path('<str:username>/', views.user_posts, name='user_posts'),
    path('<str:username>/<path:profile_picture_url>/', views.user_posts, name='user_posts_with_picture'),  # Rename if needed
]


