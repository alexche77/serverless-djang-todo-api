from rest_framework import permissions, viewsets, decorators, response

from core.mixins import ResponseGenericViewMixin
from gallery.models import Image
from gallery.serializers import ImageSerializer


@decorators.api_view(['POST'])
def create_temp_file_for_upload(request):
    return response.Response(data={'message': 'Hi'})


class ImageViewSet(
    ResponseGenericViewMixin,
    viewsets.ModelViewSet
):
    serializer_class = ImageSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Image.objects.all().order_by("-id")
