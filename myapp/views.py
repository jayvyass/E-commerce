from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from .forms import ContactForm , TestimonialForm , UserRegistrationForm 
from .models import Organic_Product ,Feature , Discount , Facts , Banner , Testimonial , CartItem
from django.contrib.auth import login
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def index(request):

    category = request.GET.get('category', 'all')
    features = Feature.objects.all()[:4]
    discounts = Discount.objects.all()[:4]
    facts = Facts.objects.all()[:4]
    banners  = Banner.objects.all()[:1]
    reviews = Testimonial.objects.order_by('?')[:6]
    # Get all products or filter by category
    if category == 'all':
        products = Organic_Product.objects.all()[4:12]  # Limit to 12 products
    elif category == 'VEG':
        products = Organic_Product.objects.filter(category='VEG')[:8]
    elif category == 'FRUIT':
        products = Organic_Product.objects.filter(category='FRUIT')[:8]
    else:
        products = Organic_Product.objects.all()[:12]

    return render(request, 'index.html', {
        'products': products,
        'category': category,
        'features': features,
        'discounts': discounts,
        'facts': facts,
        'banners': banners,
        'reviews': reviews,
    })

def vegetable(request):

    # Query the database for products with category 'Fruit'
    vegetable_products = Organic_Product.objects.filter(category='VEG')[:20]
    # Render the template and pass the products
    return render(request, 'vegetable.html', {'vegetable_products': vegetable_products})


def fruits(request):

    # Query the database for products with category 'Fruit'
    fruit_products = Organic_Product.objects.filter(category='FRUIT')[:20]
    # Render the template and pass the products
    return render(request, 'fruits.html', {'fruit_products': fruit_products})

def product_detail(request, product_id):
    # Fetch the specific product based on the provided product_id
    product = get_object_or_404(Organic_Product, product_id=product_id)
    # Fetch related products based on some criteria, e.g., same category
    related_products = Organic_Product.objects.filter(category=product.category).exclude(product_id=product_id)[:4]
    reviews = Testimonial.objects.order_by('?')[:2]

    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
             form.save()
             return redirect('index')
    else:
        form = TestimonialForm()

    return render(request, 'product-detail.html', {
        'product': product,
        'related_products': related_products,
        'form': form,
        'reviews': reviews
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Organic_Product, product_id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}  # Default quantity
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(('cart'))

@login_required(login_url='register')
def cart(request):
    cartitems = CartItem.objects.filter(user=request.user)
    subtotal = sum(Decimal(cartitem.product.price) * cartitem.quantity for cartitem in cartitems)

    # Define a flat shipping rate as a Decimal
    shipping_rate = Decimal('3.00')

    # Calculate the total using Decimal
    total = subtotal + shipping_rate

    # Prepare cart items with individual total price for each item
    cartitems_with_totals = [
        {
            'product': cartitem.product,
            'quantity': cartitem.quantity,
            'total': Decimal(cartitem.product.price) * cartitem.quantity
        }
        for cartitem in cartitems
    ]

    # Render the cart template with cart items, subtotal, and total
    return render(request, 'cart.html', {
        'cartitems': cartitems_with_totals,
        'subtotal': subtotal,
        'total': total
    })

def checkout(request):
    return render(request , 'checkout.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to the same page or another page after successful submission
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def testimonial(request):
    reviews =  Testimonial.objects.order_by('?')[:6]
    return render(request , 'testimonial.html',{'reviews': reviews})

def error(request, exception=None):
    return render(request, '404.html', status=404)

def policy(request):
    return render(request , 'policy.html')

def terms(request):
    return render(request , 't&c.html')
   
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')  # Redirect to the home page or wherever you want
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

