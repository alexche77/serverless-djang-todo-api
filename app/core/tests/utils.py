from rest_framework.authtoken.models import Token


class AuthUtils:

    @classmethod
    def sign_in(cls, test, user):
        token = Token.objects.create(user=user).key
        test.client.credentials(
            HTTP_AUTHORIZATION=f'Token {token}',
        )
