from rest_framework import routers


from user.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='users')

urlpatterns = router.urls
