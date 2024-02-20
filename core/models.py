from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.db.models import Q

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    is_public = models.BooleanField(default=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)  

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    def __str__(self):
        return self.username

class FollowersCount(models.Model):   
    follower = models.CharField(max_length=100, default='name')
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, default=None, blank=True, null=True, related_name="comment_parent")

    def __str__(self):
        return self.user.username

    def soft_delete(self):
        self.active = False
        self.save()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# class Hashtags(models.Model):
#     post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="hashtag")
#     hashtages = models.TextField()