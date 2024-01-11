from django.test import TestCase

from django.contrib.auth import get_user_model
from .models import Profile, Post, LikePost, FollowersCount, Message

User = get_user_model()

class YourAppTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)
        self.post = Post.objects.create(user='testuser', caption='Test Caption')
        self.like_post = LikePost.objects.create(post_id=str(self.post.id), username='testuser')
        self.followers_count = FollowersCount.objects.create(follower='testuser', user='anotheruser')
        self.message = Message.objects.create(sender=self.user, recipient=self.user, body='Test Message')

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.id_user, self.user.id)

    def test_post_creation(self):
        post = Post.objects.get(user='testuser')
        self.assertEqual(post.caption, 'Test Caption')

    def test_like_post_creation(self):
        like_post = LikePost.objects.get(post_id=str(self.post.id), username='testuser')
        self.assertIsNotNone(like_post)

    def test_followers_count_creation(self):
        followers_count = FollowersCount.objects.get(follower='testuser', user='anotheruser')
        self.assertIsNotNone(followers_count)

    def test_message_creation(self):
        message = Message.objects.get(sender=self.user, recipient=self.user, body='Test Message')
        self.assertIsNotNone(message)

