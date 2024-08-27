from django.contrib import admin
from .models import CartItem, Coupon, BillingDetail, Contact, Organic_Product , Feature , Discount , Facts , Banner , Testimonial , Subscriber
import csv
from django.http import HttpResponse
from datetime import datetime

# CSV export action for Organic_Product
def export_products_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Product ID', 'Name', 'Price','weight','country', 'Category', 'Out of Stock', 'created_at'])
    
    for product in queryset:
        writer.writerow([
            product.product_id,
            product.name, 
            product.price,
            product.weight,
            product.country, 
            product.category, 
            product.out_of_stock,
            product.created_at
        ])    
    return response
export_products_csv.short_description = "Export Selected Products as CSV"

# CSV export action for BillingDetail
def export_billing_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="billing_details.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Products', 'Subtotal', 'Discount', 'Total', 'User', 'Country', 'Created At'])
    
    for billing in queryset:
        writer.writerow([
            billing.id,
            billing.products,
            billing.subtotal,
            billing.discount,
            billing.total,
            billing.user,
            billing.country,
            billing.created_at
        ])
    return response
export_billing_csv.short_description = "Export Selected Billing Details as CSV"

# Registering Contact model
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')

@admin.register(Organic_Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id','name', 'price', 'category', 'out_of_stock')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    actions = [export_products_csv]

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
    actions = [export_billing_csv] 

@admin.register(Subscriber)
class SubcriberAdmin(admin.ModelAdmin):
    list_display =('email','subscribed_at')