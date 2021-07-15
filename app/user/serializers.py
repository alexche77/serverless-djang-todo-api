import logging

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import serializers
from dj_rest_auth.serializers import PasswordChangeSerializer


logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User object"""

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'date_joined'
        ]
        read_only_fields = [
            'id',
            'email',
            'date_joined'
        ]


class MyselfSerializer(serializers.ModelSerializer):

    @staticmethod
    def validate_username(username):
        if 'allauth.account' not in settings.INSTALLED_APPS:
            # We don't need to call the all-auth
            # username validator unless its installed
            return username

        from allauth.account.adapter import get_adapter
        username = get_adapter().clean_username(username)
        return username

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'date_joined'
        ]
        read_only_fields = [
            'id',
            'username',
            'email',
            'is_staff',
            'is_active',
            'date_joined'
        ]


class MyPasswordChangeSerializer(PasswordChangeSerializer):

    def save(self):
        user = self.context['request'].user
        user.auth_token.delete()
        super().save()
