from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify

class Post(models.Model):
    body = models.TextField()
    title = models.CharField(max_length=75)
    slug = models.SlugField(unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default="ashu.png", blank=True, upload_to='banners/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate unique slug only if it doesn't exist
            self.slug = slugify(f"{self.title}-{str(uuid.uuid4())}")
        super(Post, self).save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile.png', blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
     
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"

def get_default_user():
    return User.objects.get(username="default_user")

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set', null = 'True')  # Ensure unique related_name
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set', null = 'True')  # Ensure unique related_name

    def __str__(self):
        return f"{self.follower} follows {self.followed}"