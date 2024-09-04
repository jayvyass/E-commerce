from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
    path('', views.index , name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact_view, name='contact'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('fruits/', views.fruits, name='fruits'),
    path('vegetable/', views.vegetable, name='vegetable'),
    path('policy/', views.policy, name='policy'),
    path('terms&condition/', views.terms, name='terms'),
    path('product/<int:product_id>', views.product_detail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('update-cart-quantity/', views.update_cart_quantity, name='update-cart-quantity'),
    path('product/<int:product_id>/add-to-cart/', views.add_to_cart, name='add-to-cart'), 
    path('remove-cart-item/', views.remove_cart_item, name='remove_cart_item'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('search/', views.search_results, name='search_results'),
    path('404/', views.error, name='error'),

    # API
    path('api/products/', views.ProductListView.as_view(), name='product-list'),
    path('api/billing/', views.BillingDetailView.as_view(), name='Billing-list'),
    path('api/products/<int:pk>/', views.ProductDetailView.as_view(), name='products-detail'),
    path('api/billing/<int:pk>/', views.BillingDetailListView.as_view(), name='Billing-detail'),
]
handler404 = 'myapp.views.error'
