from django.urls import path 
from . import views


app_name = 'orders'
urlpatterns = [
    path('create/', views.create_order_view, name='create_order_view'),
]

