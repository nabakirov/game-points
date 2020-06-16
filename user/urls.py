from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

router = DefaultRouter()

router.register('users', views.UsersView, 'users')


urlpatterns = [
    path('v1/login/', views.LoginView.as_view(), name='login'),
    path('v1/signup/', views.SignUpView.as_view(), name='signup'),
    path('v1/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/verify/', jwt_views.token_verify),
    path('v1/', include(router.urls))
]
