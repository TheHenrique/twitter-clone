from rest_framework import serializers

from twitter.models import Tweet

from .comment_serializer import CommentSerializer


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Tweet
        fields = (
            "id",
            "user",
            "body",
            "created_at",
            "likes_count",
            "is_liked",
            "comments",
        )
        read_only_fields = ("id", "user", "created_at")

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False