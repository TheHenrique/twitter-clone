from rest_framework import serializers

from twitter.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "profile_image",
            "profile_bio",
            "homepage_link",
            "facebook_link",
            "instagram_link",
            "linkedin_link",
            "followers_count",
            "following_count",
            "is_following",
        )
        read_only_fields = ("id", "username")

    def get_followers_count(self, obj):
        return obj.followed_by.count()

    def get_following_count(self, obj):
        return obj.follows.count()

    def get_is_following(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return request.user.profile.follows.filter(id=obj.id).exists()
        return False