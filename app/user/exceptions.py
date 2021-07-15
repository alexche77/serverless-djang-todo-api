from rest_framework.exceptions import APIException
from rest_framework import status


class UserError(APIException):
    """Base exception of candidate app."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid data was provided.'


class UserDeletionError(UserError):
    """Raise when trying to delete a User."""
    default_detail = 'User deletion failed.'


class UserDoesNotExistError(UserError):
    """Raise when trying to get an nonexisting User."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'User does not exist.'
