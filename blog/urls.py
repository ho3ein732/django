from django.urls import path
from api import views
app_name = 'blog'

urlpatterns = [


    # region blog
    path('blog-list/', views.BlogListApiView.as_view(), name='blog_list'),
    path('blog-detail/<pk>/', views.BlogDetailApiView.as_view(), name='blog_detail'),
    # endregion

]