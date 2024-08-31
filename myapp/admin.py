from django.contrib import admin
from .models import Category1,Category2, CartItem, Coupon, BillingDetail, Contact, Products , Feature , Discount , Facts , Banner , Testimonial , Subscriber
import csv
from django import forms
from django.utils import timezone
from django.http import HttpResponse
from datetime import timedelta

class TotalAmountFilter(admin.SimpleListFilter):
    title = 'Total Amount'
    parameter_name = 'total_amount'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Less than $50'),
            ('medium', 'Between $50 and $100'),
            ('high', 'More than $100'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'low':
            return queryset.filter(total__lt=500)
        elif value == 'medium':
            return queryset.filter(total__gte=50, total__lte=100)
        elif value == 'high':
            return queryset.filter(total__gt=100)
        return queryset


class BillingDateFilter(admin.SimpleListFilter):
    title = 'Billing Date'
    parameter_name = 'billing_date'

    def lookups(self, request, model_admin):
        return [
            ('last_1_month', 'Last 1 month'),
            ('last_3_months', 'Last 3 months'),
            ('last_6_months', 'Last 6 months'),
            ('last_year', 'Last year')
        ]

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'last_1_month':
            start_date = today - timedelta(days=30)
            return queryset.filter(created_at__gte=start_date)
        if self.value() == 'last_3_months':
            start_date = today - timedelta(days=90)
            return queryset.filter(created_at__gte=start_date)
        if self.value() == 'last_6_months':
            start_date = today - timedelta(days=180)
            return queryset.filter(created_at__gte=start_date)
        if self.value() == 'last_year':
            start_date = today - timedelta(days=365)
            return queryset.filter(created_at__gte=start_date)
        return queryset


# CSV export action for Organic_Product

def export_products_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Product ID', 'Name', 'Price', 'Weight', 'Country', 'Categories', 'Out of Stock', 'Created At'])
    
    for product in queryset:
        if product.category2 and product.category1:
            category_display = f'{product.category2.get_full_category_name()} > {product.name}'
        elif product.category2:
            category_display = f'{product.category2.get_full_category_name()} > {product.name}'
        else:
            category_display = 'N/A'
        
        writer.writerow([
            product.product_id,
            product.name,
            product.price,
            product.weight,
            product.country,
            category_display,
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

@admin.register(Category1)
class Category1Admin(admin.ModelAdmin):
    list_display = ( 'name',)
    search_fields = ('name',)

@admin.register(Category2)
class Category2Admin(admin.ModelAdmin):
    list_display = ('get_full_category_name',)
    search_fields = ('name',)
    list_filter = ('parent_category',)

    def get_full_category_name(self, obj):
        return f"{obj.parent_category.name} > {obj.name}"
    
    get_full_category_name.short_description = 'Category'

    
class ProductForm(forms.ModelForm):
    category2 = forms.ModelChoiceField(
        queryset=Category2.objects.all(),
        label="Category2",
        empty_label="Select Category",
        widget=forms.Select
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the initial queryset for category2 and display full category names
        self.fields['category2'].queryset = Category2.objects.all()
        self.fields['category2'].widget = forms.Select(
            choices=[(cat.id, cat.get_full_category_name()) for cat in self.fields['category2'].queryset]
        )

        # If an instance exists (e.g., during form editing), set category1 based on category2
        if self.instance and self.instance.pk:
            if self.instance.category2:
                self.fields['category1'].initial = self.instance.category2.parent_category

    class Meta:
        model = Products
        fields = '__all__'
        widgets = {
            'category1': forms.HiddenInput(),  # Hide category1 field from the form
        }

    def clean(self):
        cleaned_data = super().clean()
        category2 = cleaned_data.get('category2')

        if category2:
            # Automatically set category1 based on the selected category2
            cleaned_data['category1'] = category2.parent_category

        return cleaned_data

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name','category1', 'price', 'get_category2_display', 'out_of_stock')
    list_filter = ('category1',)
    search_fields = ('name', 'description')
    actions = [export_products_csv]

    def get_category2_display(self, obj):
        if obj.category2 and obj.category1:
            return f'{obj.category2.get_full_category_name()} > {obj.name}'
        elif obj.category2:
            return f'{obj.category2.get_full_category_name()} > {obj.name}'
        return 'N/A'
    
    get_category2_display.short_description = 'Category2'


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
    list_filter = ('rating',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity','subtotal','discount','total')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_name', 'discount_percentage')

@admin.register(BillingDetail)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('id','products','subtotal','discount','total','user', 'country', 'created_at')
    actions = [export_billing_csv] 
    list_filter = (BillingDateFilter,  TotalAmountFilter) 
    
@admin.register(Subscriber)
class SubcriberAdmin(admin.ModelAdmin):
    list_display =('email','subscribed_at')