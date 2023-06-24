from rest_framework import viewsets
from social.models import Profile, Post
from social.serializers import (
    ProfileSerializer,
    PostSerializer,
    ProfileDetailSerializer,
    PostCreateUpdateSerializer,
    ProfileCreateUpdateSerializer
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        gender = self.request.query_params.get("gender")

        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        if gender:
            queryset = queryset.filter(gender=gender)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProfileDetailSerializer

        if self.action in ["create", "update"]:
            return ProfileCreateUpdateSerializer

        return self.serializer_class


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        hashtag = self.request.query_params.get("hashtag")
        title = self.request.query_params.get("title")

        queryset = self.queryset

        if hashtag:
            queryset = queryset.filter(hashtag__icontains=hashtag)

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.distinct()

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostSerializer

        if self.action in ["create", "update"]:
            return PostCreateUpdateSerializer

        return self.serializer_class
