from django.urls import path
from api import views

app_name = 'shop'

urlpatterns = [
    path('list/', views.ListShopApiView.as_view(), name='shop_list'),
    path('detail/', views.DetailShopApiView.as_view(), name='shop_detail'),
]
