from rest_framework import status
from rest_framework.response import Response as ErrorResponse
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Exception handler to make all error responses."""
    old_response = exception_handler(exc, context)  # get original response
    old_status_code = getattr(
        old_response,
        'status_code',
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    # Early termination if items is empty
    if not old_response or not old_response.data.items():
        return ErrorResponse(status=old_status_code)

    errors = [
        {
            'status': getattr(exc, 'status_code', old_status_code),
            'type': str(exc.__class__.__name__),
            'title': getattr(exc, 'default_detail', str(exc)),
            'source': source,
            'description': error,
        }
        for (source, error) in old_response.data.items()
    ]

    return ErrorResponse(data={'errors': errors}, status=old_status_code)


def get_validated_data(Serializer, data):
    """Evaluate if given data is valid usign a serializer"""
    serializer = Serializer(data=data)
    serializer.is_valid(raise_exception=True)

    return serializer.validated_data
