from rest_framework import routers
from django.urls import path


from gallery.views import ImageViewSet, create_temp_file_for_upload

router = routers.DefaultRouter()
router.register(r'gallery', ImageViewSet, basename='gallery')

urlpatterns = router.urls + [
    path('tmp/upload_url', create_temp_file_for_upload)
]
