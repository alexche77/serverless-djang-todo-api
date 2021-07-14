from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('', view=views.UserListView.as_view(), name='index'),
    path('token', view=views.CreateTokenView.as_view(), name='token'),
    path('me', view=views.ManageUserView.as_view(), name='me'),
]
