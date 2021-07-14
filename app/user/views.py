from django.contrib.auth import get_user_model

from rest_framework import authentication, permissions
from rest_framework.generics import CreateAPIView,\
    ListAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class UserListView(CreateAPIView, ListAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user
