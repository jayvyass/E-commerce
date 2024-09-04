from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField 
from decimal import Decimal

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class Category1(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category2(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(Category1, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name
    
    def get_full_category_name(self):
        return f"{self.parent_category.name} > {self.name}"

class Products(models.Model):
    
    product_id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category1 = models.ForeignKey(Category1, on_delete=models.SET_NULL, null=True, blank=True)
    category2 = models.ForeignKey(Category2, on_delete=models.SET_NULL, null=True, blank=True)
    weight = models.CharField(max_length=50, null=True, blank=True)  # Weight with unit (e.g., "1 kg", "1 piece")
    country = models.CharField(max_length=255, null=True, blank=True)  # Country of origin
    out_of_stock = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    def update_totals(self):
        if self.subtotal == self.total:
            self.discount = Decimal('0.00')
        else:
            self.discount = self.subtotal - self.total
        self.save()

class Feature(models.Model):
    feature_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)  # Use a CharField for the icon as a text input
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title    

class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='discounts/images/')  # Field for uploading images
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title

class Facts(models.Model):
    facts_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)  # Field for storing icon names or paths
    information = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title

class Banner(models.Model):
    banner_id = models.AutoField(primary_key=True)  # Primary key field
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/images/')  # Field for uploading images
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Field for price
    quantity = models.PositiveIntegerField()  # Field for quantity
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title    

class Testimonial(models.Model):
    testimonial_id = models.AutoField(primary_key=True)  # Primary key field
    name = models.CharField(max_length=255)  # Field for the name of the person giving the testimonial
    email = models.EmailField()  # Field for the email of the person giving the testimonial
    review = models.TextField()  # Field for the testimonial review
    rating = models.PositiveIntegerField()  # Field for rating (ensure it is an integer)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Testimonial by {self.name}"
    

class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)  # Primary key field
    coupon_name = models.CharField(max_length=255)  # Field for the name of the coupon
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Field for the discount percentage
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Coupon: {self.coupon_name} - {self.discount_percentage}%"

class BillingDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=255, blank=False)
    town_city = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=100, blank=False)
    postcode_zip = models.CharField(max_length=20, blank=False)
    mobile = models.CharField(max_length=15, blank=False)
    email = models.EmailField(blank=False)
    order_notes = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    products = JSONField(default=dict, blank=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subscriber(models.Model):
    email = models.EmailField(unique=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

