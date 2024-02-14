from django.urls import include, path
from rest_framework import routers

from api_users.views import UserViewSet
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from api.views import CommentViewSet, ReviewViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
