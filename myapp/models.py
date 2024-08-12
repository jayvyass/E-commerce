from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Organic_Product(models.Model):
    PRODUCT_CATEGORY_CHOICES = [
        ('VEG', 'Vegetable'),
        ('FRUIT', 'Fruit'),
    ]
    product_id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/images/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=5,
        choices=PRODUCT_CATEGORY_CHOICES,
        default='FRUIT',  # Default to 'Fruit'
    )
    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Organic_Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Feature(models.Model):
    feature_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)  # Use a CharField for the icon as a text input
    description = models.TextField()

    def __str__(self):
        return self.title    

class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='discounts/images/')  # Field for uploading images
    description = models.TextField()

    def __str__(self):
        return self.title

class Facts(models.Model):
    facts_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)  # Field for storing icon names or paths
    information = models.TextField()

    def __str__(self):
        return self.title

class Banner(models.Model):
    banner_id = models.AutoField(primary_key=True)  # Primary key field
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/images/')  # Field for uploading images
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Field for price
    quantity = models.PositiveIntegerField()  # Field for quantity

    def __str__(self):
        return self.title    

class Testimonial(models.Model):
    testimonial_id = models.AutoField(primary_key=True)  # Primary key field
    name = models.CharField(max_length=255)  # Field for the name of the person giving the testimonial
    email = models.EmailField()  # Field for the email of the person giving the testimonial
    review = models.TextField()  # Field for the testimonial review
    rating = models.PositiveIntegerField()  # Field for rating (ensure it is an integer)

    def __str__(self):
        return f"Testimonial by {self.name}"
    

class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)  # Primary key field
    coupon_name = models.CharField(max_length=255)  # Field for the name of the coupon
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Field for the discount percentage

    def __str__(self):
        return f"Coupon: {self.coupon_name} - {self.discount_percentage}%"
