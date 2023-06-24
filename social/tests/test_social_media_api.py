from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from social.models import Profile, Post
from social.serializers import ProfileSerializer, ProfileDetailSerializer, PostSerializer, PostCreateUpdateSerializer

PROFILE_URL = reverse("social:profile-list")
POST_URL = reverse("social:post-list")


def sample_profile(**params):
    defaults = {
        "user": "",
        "first_name": "firstname",
        "last_name": "lastname",
        "gender": "Female",
    }
    defaults.update(params)

    return Profile.objects.create(**defaults)


def sample_post(**params):
    defaults = {
        "author": "",
        "profile": "",
        "title": "firstname",
        "content": "lastname",
    }
    defaults.update(params)

    return Post.objects.create(**defaults)


def profile_detail_url(profile_id):
    return reverse("social:profile-detail", args=[profile_id])


def post_detail_url(post_id):
    return reverse("social:post-detail", args=[post_id])


class ProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass1",
        )
        self.client.force_authenticate(self.user)

    def test_list_profiles(self):
        user = get_user_model().objects.create_user(
            "tes1t@test.com",
            "testpass1",
        )
        sample_profile(user=user)
        sample_profile(user=self.user)
        res = self.client.get(PROFILE_URL)

        profiles = Profile.objects.order_by("id")
        serializer = ProfileSerializer(profiles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_profiles_by_genders(self):
        user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass1",
        )
        user1 = get_user_model().objects.create_user(
            "test2@test.com",
            "testpass1",
        )
        profile1 = sample_profile(user=user, gender="Female")
        profile2 = sample_profile(user=user1, gender="Male")
        profile3 = sample_profile(user=self.user, gender="unknown")

        res = self.client.get(PROFILE_URL, {"gender": "Female"})

        serializer1 = ProfileSerializer(profile1)
        serializer2 = ProfileSerializer(profile2)
        serializer3 = ProfileSerializer(profile3)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_profiles_by_first_name(self):
        user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass1",
        )
        user1 = get_user_model().objects.create_user(
            "test2@test.com",
            "testpass1",
        )
        profile1 = sample_profile(user=user, first_name="Yuriy")
        profile2 = sample_profile(user=user1, first_name="Ivan")
        profile3 = sample_profile(user=self.user, first_name="Roman")

        res = self.client.get(PROFILE_URL, {"first_name": "Yuriy"})

        serializer1 = ProfileSerializer(profile1)
        serializer2 = ProfileSerializer(profile2)
        serializer3 = ProfileSerializer(profile3)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_profiles_by_last_name(self):
        user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass1",
        )
        user1 = get_user_model().objects.create_user(
            "test2@test.com",
            "testpass1",
        )
        profile1 = sample_profile(user=user, last_name="Lastone")
        profile2 = sample_profile(user=user1, last_name="Lasttwo")
        profile3 = sample_profile(user=self.user, last_name="Last")

        res = self.client.get(PROFILE_URL, {"last_name": "Lastone"})

        serializer1 = ProfileSerializer(profile1)
        serializer2 = ProfileSerializer(profile2)
        serializer3 = ProfileSerializer(profile3)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_profile_detail(self):
        profile = sample_profile(
            user=self.user,
        )

        url = profile_detail_url(profile.id)
        res = self.client.get(url)

        serializer = ProfileDetailSerializer(profile)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_another_profile_forbidden(self):

        user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass1",
        )

        profile = sample_profile(user=user)
        payload = {
            "first_name": "another",
            "last_name": "another",
            "gender": "Male",
        }
        res = self.client.put(profile_detail_url(profile.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_another_profile_forbidden(self):
        user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass1",
        )
        profile = sample_profile(user=user)
        res = self.client.delete(profile_detail_url(profile.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PostsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass1",
        )
        self.profile = sample_profile(user=self.user)
        self.client.force_authenticate(self.user)

    def test_list_posts(self):
        sample_post(author=self.user, profile=self.profile)
        sample_post(author=self.user, profile=self.profile)
        res = self.client.get(POST_URL)

        posts = Post.objects.order_by("id")
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_post_by_title(self):
        post1 = sample_post(author=self.user, profile=self.profile, title="title1")
        post2 = sample_post(author=self.user, profile=self.profile, title="title2")
        post3 = sample_post(author=self.user, profile=self.profile, title="title3")

        res = self.client.get(POST_URL, {"title": "title1"})

        serializer1 = PostSerializer(post1)
        serializer2 = PostSerializer(post2)
        serializer3 = PostSerializer(post3)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_post_by_hashtag(self):
        post1 = sample_post(author=self.user, profile=self.profile, hashtag="hashtag1")
        post2 = sample_post(author=self.user, profile=self.profile, hashtag="hashtag2")
        post3 = sample_post(author=self.user, profile=self.profile, hashtag="hashtag3")

        res = self.client.get(POST_URL, {"hashtag": "hashtag1"})

        serializer1 = PostSerializer(post1)
        serializer2 = PostSerializer(post2)
        serializer3 = PostSerializer(post3)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_post_detail(self):
        post = sample_post(author=self.user, profile=self.profile)

        url = post_detail_url(post.id)
        res = self.client.get(url)

        serializer = PostSerializer(post)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_another_post_forbidden(self):

        user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass1",
        )

        profile = sample_profile(user=user)
        post = sample_post(author=user, profile=profile)
        payload = {
            "title": "another",
            "content": "another",
            "hashtag": "test",
        }
        res = self.client.put(post_detail_url(post.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_another_profile_forbidden(self):
        user = get_user_model().objects.create_user(
            "test1@test.com",
            "testpass1",
        )
        profile = sample_profile(user=user)
        post = sample_post(author=user, profile=profile)
        res = self.client.delete(post_detail_url(post.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
