from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from twitter.viewsets import CommentViewSet, ProfileViewSet, TweetViewSet
from twitter.views_api import RegisterAPIView

router = DefaultRouter()
router.register("tweets", TweetViewSet, basename="tweet")
router.register("comments", CommentViewSet, basename="comment")
router.register("profiles", ProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", RegisterAPIView.as_view(), name="api_register"),
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
]