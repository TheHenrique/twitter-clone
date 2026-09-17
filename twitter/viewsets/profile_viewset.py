from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from twitter.models import Profile
from twitter.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def follow(self, request, pk=None):
        profile = self.get_object()
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        return Response({"status": "following"})

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def unfollow(self, request, pk=None):
        profile = self.get_object()
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        return Response({"status": "unfollowed"})