from django.urls import path
from . import views
 

urlpatterns = [
    path('', views.index , name='index'),
    path('register/', views.register, name='register'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact_view, name='contact'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('fruits/', views.fruits, name='fruits'),
    path('vegetable/', views.vegetable, name='vegetable'),
    path('policy/', views.policy, name='policy'),
    path('terms&condition/', views.terms, name='terms'),
    path('product/<int:product_id>', views.product_detail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:product_id>/add-to-cart/', views.add_to_cart, name='add-to-cart'), 
    path('404/', views.error, name='error'),
]
handler404 = 'myapp.views.error'
