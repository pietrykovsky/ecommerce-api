from rest_framework import routers

from django.urls import path, include

from shop import views

app_name = 'shop'

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]