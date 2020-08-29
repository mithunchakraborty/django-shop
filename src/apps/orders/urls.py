from django.urls import path 
from . import views


app_name = 'orders'
urlpatterns = [
    path('create/', views.create_order_view, name='create_order_view'),
    path(
        'admin/order/<int:order_id>', 
        views.admin_order_detail_view, 
        name='admin_order_detail_view'
    )
]

