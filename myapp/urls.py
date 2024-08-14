from django.urls import path
from . import views
 

urlpatterns = [
    path('', views.index , name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact_view, name='contact'),
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
    path('404/', views.error, name='error'),
]
handler404 = 'myapp.views.error'
