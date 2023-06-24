from rest_framework import serializers

from social.models import Profile, Post
from user.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "full_name",
            "avatar",
            "gender",
            "followers_count",
            "posts_count",
        )

    @staticmethod
    def get_followers_count(obj):
        return obj.user.followers.count()

    @staticmethod
    def get_posts_count(obj):
        return obj.posts.count()


class ProfilePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "created_at",)


class ProfileDetailSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    user = UserSerializer(many=False, read_only=True)
    posts = ProfilePostsSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "posts",
            "first_name",
            "last_name",
            "avatar",
            "biography",
            "gender",
            "following",
            "followers",
        )

    @staticmethod
    def get_followers(obj):
        return [
            followed_user.full_name for followed_user in obj.user.followers.all()
        ]

    @staticmethod
    def get_following(obj):
        return [
            following_user.profiles.full_name for following_user in obj.following.all()
        ]


class ProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "avatar",
            "gender",
            "following",
        )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="profile.full_name")
    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "media_attachments",
            "hashtag",
            "created_at",
        )
        read_only_fields = [
            "author",
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "profile",
            "title",
            "content",
            "media_attachments",
            "hashtag",
            "created_at",
        )
        read_only_fields = [
            "author",
            "profile",
        ]
