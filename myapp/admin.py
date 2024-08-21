from django.contrib import admin
from .models import CartItem, Coupon, BillingDetail, Contact, Organic_Product , Feature , Discount , Facts , Banner , Testimonial

# Registering Contact model
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')

@admin.register(Organic_Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id','name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'description')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description')

@admin.register(Facts)
class FactAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'information')    

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description')    

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating')   

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity','subtotal','discount','total')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_name', 'discount_percentage')

@admin.register(BillingDetail)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('id', 'products','subtotal','discount','total','user', 'country')