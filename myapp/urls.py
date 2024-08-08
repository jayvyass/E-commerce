from django.urls import path
from . import views
 

urlpatterns = [
    path('', views.index , name='index'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact_view, name='contact'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('fruits/', views.fruits, name='fruits'),
    path('vegetable/', views.vegetable, name='vegetable'),
    path('policy/', views.policy, name='policy'),
    path('terms&condition/', views.terms, name='terms'),
    path('product/<int:product_id>/', views.product_detail, name='product-detail'),
    path('404/', views.error, name='error'),
]
handler404 = 'myapp.views.error'