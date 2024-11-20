# inventory/urls.py
from django.urls import path
from inventory import views

urlpatterns = [
    # path('', views.user_login, name='login'),
    path("dash/", views.index, name="dash"),
    path("products/", views.products, name="products"),
    path("product/", views.product, name="product"),
    path('delete_item/', views.delete_item, name='delete_item'),
    path("users/", views.users, name="users"),
    path("user/", views.user, name="user"),
    path("register/", views.register_user, name="register"),
    path("client/", views.client, name="client"),
    path("clients/", views.clients, name="clients"),
    path("crfq/",views.crfq,name="crfq"),
    # path("view_rfq/",views.view_rfq,name="view_rfq"),
    path('orders/', views.orders, name='orders'),
    path('clear_data/', views.clear_data, name='clear_data'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('delete_client/', views.delete_client, name='delete_client'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('update/<int:cid>/', views.update_client, name='update_client'),
    path('update_user/<int:id>/', views.update_user, name='update_user'),
    path('update_item/<int:id>/', views.update_item, name='update_item'),
    path('change_password', views.change_password, name='change_password'),
]
