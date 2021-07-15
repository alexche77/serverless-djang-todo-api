import logging
from django.contrib.auth.models import User

from rest_framework import permissions, viewsets

from user.serializers import UserSerializer
from core.mixins import ResponseGenericViewMixin


logger = logging.getLogger(__name__)


class UserViewSet(
    ResponseGenericViewMixin,
    viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().order_by("-id")
