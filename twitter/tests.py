from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .forms import SignUpForm
from .models import Comment, Profile, Tweet


class TweetModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="senha12345678")

    def test_str_returns_formatted_text(self):
        tweet = Tweet.objects.create(user=self.user, body="meu primeiro tweet")
        self.assertIn("alice", str(tweet))
        self.assertIn("meu primeiro tweet", str(tweet))

    def test_number_of_likes(self):
        tweet = Tweet.objects.create(user=self.user, body="tweet com likes")
        other = User.objects.create_user("bob", password="senha12345678")
        tweet.likes.add(other)
        self.assertEqual(tweet.number_of_likes(), 1)


class ProfileSignalTests(TestCase):
    def test_profile_created_and_follows_self(self):
        user = User.objects.create_user("alice", password="senha12345678")
        self.assertTrue(Profile.objects.filter(user=user).exists())
        profile = Profile.objects.get(user=user)
        self.assertTrue(profile.follows.filter(id=profile.id).exists())


class SignUpFormTests(TestCase):
    def test_password_not_required_when_editing(self):
        user = User.objects.create_user("alice", password="senha12345678")
        form = SignUpForm(
            data={
                "username": "alice",
                "first_name": "Alice",
                "last_name": "Silva",
                "email": "alice@example.com",
            },
            instance=user,
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Alice")

    def test_password_required_when_creating(self):
        form = SignUpForm(
            data={
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)


class FeedTests(TestCase):
    def test_feed_shows_only_followed_users_tweets(self):
        alice = User.objects.create_user("alice", password="senha12345678")
        bob = User.objects.create_user("bob", password="senha12345678")

        tweet_alice = Tweet.objects.create(user=alice, body="tweet da alice")
        tweet_bob = Tweet.objects.create(user=bob, body="tweet do bob")

        following_ids = alice.profile.follows.values_list("user_id", flat=True)
        feed = Tweet.objects.filter(user_id__in=following_ids)

        self.assertIn(tweet_alice, feed)
        self.assertNotIn(tweet_bob, feed)


class TweetAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("carol", password="senha12345678")
        self.client.force_authenticate(user=self.user)

    def test_create_tweet(self):
        response = self.client.post(
            "/api/v1/tweets/", {"body": "tweet via api"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tweet.objects.filter(user=self.user).count(), 1)

    def test_like_toggle(self):
        tweet = Tweet.objects.create(user=self.user, body="curte isso")
        response = self.client.post(f"/api/v1/tweets/{tweet.id}/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["liked"])

        response = self.client.post(f"/api/v1/tweets/{tweet.id}/like/")
        self.assertFalse(response.data["liked"])

    def test_cannot_edit_others_tweet(self):
        other = User.objects.create_user("dave", password="senha12345678")
        tweet = Tweet.objects.create(user=other, body="tweet do dave")
        response = self.client.patch(
            f"/api/v1/tweets/{tweet.id}/", {"body": "tentando editar"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_feed_endpoint_filters_by_follows(self):
        other = User.objects.create_user("dave", password="senha12345678")
        Tweet.objects.create(user=other, body="tweet do dave")
        response = self.client.get("/api/v1/tweets/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)


class CommentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("carol", password="senha12345678")
        self.tweet = Tweet.objects.create(user=self.user, body="tweet pra comentar")
        self.client.force_authenticate(user=self.user)

    def test_create_comment(self):
        response = self.client.post(
            "/api/v1/comments/",
            {"tweet": self.tweet.id, "body": "ótimo tweet!"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.filter(tweet=self.tweet).count(), 1)


class ProfileAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("carol", password="senha12345678")
        self.other = User.objects.create_user("dave", password="senha12345678")
        self.client.force_authenticate(user=self.user)

    def test_follow_and_unfollow(self):
        other_profile = Profile.objects.get(user=self.other)

        response = self.client.post(f"/api/v1/profiles/{other_profile.id}/follow/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.user.profile.follows.filter(id=other_profile.id).exists()
        )

        response = self.client.post(f"/api/v1/profiles/{other_profile.id}/unfollow/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            self.user.profile.follows.filter(id=other_profile.id).exists()
        )


class RegisterAPITests(APITestCase):
    def test_register_creates_user_and_returns_token(self):
        response = self.client.post(
            "/api/v1/auth/register/",
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "senha12345678",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertTrue(User.objects.filter(username="newuser").exists())