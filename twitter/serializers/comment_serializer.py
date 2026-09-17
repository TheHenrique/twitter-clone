from rest_framework import serializers

from twitter.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Comment
        fields = ("id", "tweet", "user", "body", "created_at")
        read_only_fields = ("id", "user", "created_at")