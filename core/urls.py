from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('confirm_order/', views.ConfirmOrderView.as_view(), name='confirm_order'),
    path('choose_delivery/', views.ChooseDeliveryView.as_view(), name='choose_delivery'),
    path('delivery_address/', views.DeliveryAddressView.as_view(), name='delivery_address'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),

   
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/products/', views.admin_products, name='admin_products'),
    path('dashboard/products/create/', views.admin_product_create, name='admin_product_create'),
    path('dashboard/products/<int:pk>/update/', views.admin_product_update, name='admin_product_update'),
    path('dashboard/products/<int:pk>/delete/', views.admin_product_delete, name='admin_product_delete'),
    path('dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('dashboard/reports/', views.admin_reports, name='admin_reports'),
    path('dashboard/reports/orders_per_day/', views.report_orders_per_day, name='report_orders_per_day'),
    path('dashboard/reports/popular_products/', views.report_popular_products, name='report_popular_products'),
    path('dashboard/reports/orders_per_product/', views.report_orders_per_product, name='report_orders_per_product'),
    path('dashboard/reports/orders_in_period/', views.report_orders_in_period, name='report_orders_in_period'),
]








# Nuevas rutas para la funcionalidad de los domiciliarios
urlpatterns += [
    path('delivery_persons/', views.list_delivery_persons, name='list_delivery_persons'),
    path('delivery_persons/new/', views.create_delivery_person, name='create_delivery_person'),
    
    path('delivery_persons/<int:pk>/delete/', views.delete_delivery_person, name='delete_delivery_person'),
]
