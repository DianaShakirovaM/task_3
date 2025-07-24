from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import ActivityFeedViewSet, CustomUserViewSet, TaskViewSet

v1_router = DefaultRouter()
v1_router.register('tasks', TaskViewSet)
v1_router.register('activity-feed', ActivityFeedViewSet, basename='activity')
v1_router.register('users', CustomUserViewSet)

urlpatterns = (
    path('auth/', include('djoser.urls')),
    path('auth/token/', views.obtain_auth_token),
    path('', include(v1_router.urls))
)
