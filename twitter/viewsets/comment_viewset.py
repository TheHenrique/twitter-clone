from rest_framework import permissions, viewsets

from twitter.models import Comment
from twitter.permissions import IsOwnerOrReadOnly
from twitter.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all()
        tweet_id = self.request.query_params.get("tweet")
        if tweet_id is not None:
            queryset = queryset.filter(tweet_id=tweet_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)