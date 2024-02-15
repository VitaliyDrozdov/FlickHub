from django.urls import include, path
from rest_framework import routers

from api_users.views import UserViewSet, SignUpView, AccessView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/', AccessView.as_view(), name='access_token'),
]
