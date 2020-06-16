from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()

router.register('transactions', views.TransactionViewSet, 'transactions')


urlpatterns = [
    path('v1/', include(router.urls), name='transactions')
]
