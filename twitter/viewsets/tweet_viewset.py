from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from twitter.models import Tweet
from twitter.permissions import IsOwnerOrReadOnly
from twitter.serializers import TweetSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by("-created_at")
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def feed(self, request):
        following_ids = request.user.profile.follows.values_list(
            "user_id", flat=True
        )
        tweets = Tweet.objects.filter(user_id__in=following_ids).order_by(
            "-created_at"
        )
        page = self.paginate_queryset(tweets)
        serializer = self.get_serializer(page if page is not None else tweets, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def like(self, request, pk=None):
        tweet = self.get_object()
        if tweet.likes.filter(id=request.user.id).exists():
            tweet.likes.remove(request.user)
            liked = False
        else:
            tweet.likes.add(request.user)
            liked = True
        return Response({"liked": liked, "likes_count": tweet.likes.count()})