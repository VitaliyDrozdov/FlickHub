
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView


from api.views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router_v1.urls)),
]


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]