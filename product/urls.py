from django.urls import path
from api import views
app_name = 'product'

urlpatterns = [
    path('products/', views.ListProductApiView.as_view(), name='products'),
    path('product/<pk>/', views.DetailProductApiView.as_view(), name='product')
]