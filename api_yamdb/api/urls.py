
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView

from api_users.views import UserViewSet
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]