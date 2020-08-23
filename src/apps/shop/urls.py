from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.get_product_list_view, name='get_product_list_view'),
    path('<slug:category_slug>/', views.get_product_list_view, name='get_product_list_view_by_category'),
    path('<int:id>@<slug:slug>/', views.get_product_detail_view, name='get_product_detail_view'),
]

