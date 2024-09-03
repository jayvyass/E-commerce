from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from django.contrib.auth import login , logout
from decimal import Decimal
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail , EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging
from io import BytesIO
from xhtml2pdf import pisa
from rest_framework import generics
from .serializers import ProductSerializer , BillingSerializer
from .decorators import unauthenticated_user
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .forms import ContactForm , TestimonialForm ,SubscribeForm, UserRegistrationForm , BillingDetailForm
from .models import Products,Category1,Category2,Subscriber ,BillingDetail,Feature ,Coupon, Discount , Facts , Banner , Testimonial , CartItem

logger = logging.getLogger(__name__)

def index(request):
    category_name = request.GET.get('category', 'all')
    query = request.GET.get('q', '')

    # Fetch common data
    features = Feature.objects.all()[:4]
    discounts = Discount.objects.all()[:4]
    facts = Facts.objects.all()[:4]
    banners = Banner.objects.all()[:1]
    reviews = Testimonial.objects.filter(rating__gt=3)[:6]

    # Fetch Category1 instances for filtering
    categories = Category1.objects.all()

    # Determine category filter
    if category_name == 'all':
        products = Products.objects.all()
    else:
        category1 = Category1.objects.filter(name=category_name).first()
        if category1:
            products = Products.objects.filter(category1=category1)
        else:
            products = Products.objects.all()  # Fallback in case of invalid category

    # Handle search query
    if query:
        products = products.filter(name__icontains=query)

    # Limit the number of products displayed
    products = products[4:12]  # Adjust the slice as needed

    # Fetch products based on fixed categories (e.g., Vegetables and Fruits)
    vegetable_category = Category1.objects.filter(name='Vegetables').first()
    fruit_category = Category1.objects.filter(name='Fruits').first()

    if vegetable_category:
        vegetable_products = Products.objects.filter(category1=vegetable_category)
        if query:
            vegetable_products = vegetable_products.filter(name__icontains=query)[:7]
        else:
            vegetable_products = vegetable_products[:7]
    else:
        vegetable_products = Products.objects.none()  # No vegetables found

    if fruit_category:
        fruit_products = Products.objects.filter(category1=fruit_category)
        if query:
            fruit_products = fruit_products.filter(name__icontains=query)[:7]
        else:
            fruit_products = fruit_products[:7]
    else:
        fruit_products = Products.objects.none()  # No fruits found

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'category': category_name,
        'features': features,
        'discounts': discounts,
        'facts': facts,
        'banners': banners,
        'reviews': reviews,
        'vegetables': vegetable_products,
        'fruits': fruit_products,
        'query': query
    })



def vegetable(request):
    query = request.GET.get('q', '')
    category1_id = Category1.objects.filter(name='Vegetables').first().id
    
    if query:
        vegetable_products = Products.objects.filter(category1_id=category1_id, name__icontains=query)[:20]
    else:
        vegetable_products = Products.objects.filter(category1_id=category1_id)[:20]

    return render(request, 'vegetable.html', {'vegetable_products': vegetable_products, 'search_query': query})

def fruits(request):
    query = request.GET.get('q', '')
    category1_id = Category1.objects.filter(name='Fruits').first().id
    
    if query:
        fruit_products = Products.objects.filter(category1_id=category1_id, name__icontains=query)[:20]
    else:
        fruit_products = Products.objects.filter(category1_id=category1_id)[:20]

    return render(request, 'fruits.html', {'fruit_products': fruit_products, 'search_query': query})

def product_detail(request, product_id):
    # Fetch the specific product based on the provided product_id
    product = get_object_or_404(Products, product_id=product_id)
    category = product.category1
    related_products = Products.objects.filter(category1=category).exclude(product_id=product_id)[:4]
    reviews = Testimonial.objects.filter(rating__gt=3).order_by('?')[:2]

    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
             form.save()
             messages.success(request, 'Thank you for your review! We appreciate your feedback.')
             return redirect('index')
    else:
        form = TestimonialForm()
    return render(request, 'product-detail.html', {
        'product': product,
        'related_products': related_products,
        'form': form,
        'reviews': reviews
    })

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, product_id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
    
    # Calculate the subtotal
    cart_item.subtotal = Decimal(cart_item.product.price) * cart_item.quantity

    # Reset the discount to zero when adding a new item unless a coupon is applied
    cart_item.discount = Decimal('0.00')

    # Update total after adding the product to the cart
    cart_item.total =  Decimal(cart_item.product.price) * cart_item.quantity
    cart_item.save()

    return redirect('cart')



@login_required(login_url='login')
@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        new_quantity = data.get('quantity')
        coupon_name = data.get('coupon_name', '').strip()

        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)

            if new_quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = new_quantity
                cart_item.subtotal = Decimal(cart_item.product.price) * new_quantity

                if coupon_name:
                    try:
                        coupon = Coupon.objects.get(coupon_name=coupon_name)
                        cart_item.discount = cart_item.subtotal * (coupon.discount_percentage / 100)
                    except Coupon.DoesNotExist:
                        cart_item.discount = Decimal('0.00')
                else:
                    cart_item.discount = Decimal('0.00')

                cart_item.total = cart_item.subtotal - cart_item.discount
                cart_item.save()

            # Recalculate overall totals
            cart_items = CartItem.objects.filter(user=request.user)
            subtotal = sum(item.subtotal for item in cart_items)
            discount = sum(item.discount for item in cart_items)
            total = subtotal - discount
            total2 = Decimal(cart_item.product.price) * new_quantity
            return JsonResponse({
                'success': True,
                'new_quantity': cart_item.quantity,
                'new_total': float(total2),
                'new_subtotal': float(subtotal),
                'discount_amount': float(discount),
                'new_total_with_shipping': float(total)
            })

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url='login')
@csrf_exempt
def remove_cart_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        coupon_name = data.get('coupon_name', '').strip()

        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
            cart_item.delete()

            # Recalculate cart totals
            cart_items = CartItem.objects.filter(user=request.user)
            subtotal = sum(item.subtotal for item in cart_items)
            discount = sum(item.discount for item in cart_items)
            total = sum(item.total for item in cart_items)

            return JsonResponse({
                'success': True,
                'new_subtotal': float(subtotal),
                'discount_amount': float(discount),
                'new_total_with_shipping': float(total)
            })

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required(login_url='login')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    # Retrieve the coupon name from the request (you can use GET or POST depending on your form setup)
    coupon_name = request.GET.get('coupon_name', '').strip()

    # If the coupon name is empty, reset the discount and total for each item
    if not coupon_name:
        cart_items.update(discount=Decimal('0.00'))
        for cart_item in cart_items:
            cart_item.total = cart_item.subtotal  # Reset total to match subtotal
            cart_item.save()

    # Calculate the subtotal (sum of all item subtotals)
    subtotal = sum(cart_item.subtotal for cart_item in cart_items)

    # Calculate the total discount applied (sum of all item discounts)
    discount = sum(cart_item.discount for cart_item in cart_items)

    # Calculate the overall total (subtotal minus discount)
    total = subtotal - discount

    cart_items_with_totals = [
        {
            'product': cart_item.product,
            'quantity': cart_item.quantity,
            'total': cart_item.total,  # This is the total for each cart item
        }
        for cart_item in cart_items
    ]

    return render(request, 'cart.html', {
        'cartitems': cart_items_with_totals,
        'subtotal': subtotal,
        'total': total,  # This is the total for the entire cart
        'discount': discount
    })



@login_required(login_url='login')
@csrf_exempt
def apply_coupon(request):
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name', '').strip()

        cart_items = CartItem.objects.filter(user=request.user)

        if not coupon_name:
            # If no coupon is provided, reset the discount and total for each item
            cart_items.update(discount=Decimal('0.00'))
            for cart_item in cart_items:
                cart_item.total = cart_item.subtotal  # Reset total to match subtotal
                cart_item.save()

            # Recalculate cart totals
            subtotal = sum(item.subtotal for item in cart_items)
            discount = sum(item.discount for item in cart_items)
            total = subtotal  # Total should match subtotal when no discount is applied

            return JsonResponse({
                'success': True,
                'discount_amount': 0.0,
                'total': float(total),
            })

        try:
            coupon = Coupon.objects.get(coupon_name=coupon_name)
            discount_percentage = coupon.discount_percentage

            for cart_item in cart_items:
                cart_item.discount = cart_item.subtotal * (discount_percentage / 100)
                cart_item.total = cart_item.subtotal - cart_item.discount
                cart_item.save()

            subtotal = sum(item.subtotal for item in cart_items)
            discount = sum(item.discount for item in cart_items)
            total = subtotal - discount

            return JsonResponse({
                'success': True,
                'discount_amount': float(discount),
                'total': float(total)
            })

        except Coupon.DoesNotExist:
            request.session['coupon_name'] = None
            return JsonResponse({'success': False, 'message': 'Invalid coupon name'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required(login_url='login')
def checkout(request):
    # Check if cart is empty
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty. Please add items to your cart before proceeding to checkout.')
        return redirect('cart')  # Redirect to your cart page

    previous_billing_detail = BillingDetail.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = BillingDetailForm(request.POST)
        if form.is_valid():
            billing_detail = form.save(commit=False)
            billing_detail.user = request.user
            billing_detail.total = request.POST.get('amount', 0)
            billing_detail.subtotal = Decimal(request.POST.get('subtotal', '0.00'))
            billing_detail.discount = Decimal(request.POST.get('discount', '0.00'))
            
            products = []
            for key in request.POST.keys():
                if key.startswith('product_name_'):
                    index = key.replace('product_name_', '')
                    product_name = request.POST.get(key)
                    product_quantity = request.POST.get(f'product_quantity_{index}', 0)
                    products.append({
                        'product_name': product_name,
                        'quantity': product_quantity
                    })

            billing_detail.products = products
            billing_detail.save()

            invoice_html = render_to_string('invoice.html', {
                'billing_detail': billing_detail,
                'products': products,
                'subtotal': billing_detail.subtotal,
                'discount': billing_detail.discount,
                'total': billing_detail.total
            })

            # Convert HTML to plain text
            invoice_plain = strip_tags(invoice_html)
            pdf_attachment = render_to_pdf(invoice_html)

            # Create and send the email
            email = EmailMultiAlternatives(
                subject='Your Invoice from Our Store',
                body=invoice_plain,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[billing_detail.email],
            )
            email.attach_alternative(invoice_html, "text/html")
            
            if pdf_attachment:
                email.attach('invoice.pdf', pdf_attachment, 'application/pdf')

            email.send()

            messages.success(request, 'Transaction completed successfully!')
            CartItem.objects.filter(user=request.user).delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        if previous_billing_detail:
            form = BillingDetailForm(instance=previous_billing_detail)
        else:
            form = BillingDetailForm()

    subtotal = sum(item.subtotal for item in cart_items)
    discount = sum(item.discount for item in cart_items)
    total = sum(item.total for item in cart_items)

    cart_items_with_totals = [
        {
            'product': cart_item.product,
            'quantity': cart_item.quantity,
            'total': Decimal(cart_item.product.price) * cart_item.quantity
        }
        for cart_item in cart_items
    ]

    return render(request, 'checkout.html', {
        'form': form,
        'cartitems': cart_items_with_totals,
        'subtotal': subtotal,
        'discount_amount': discount,
        'total': total,
        'billing_detail_exists': previous_billing_detail is not None
    })



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database

            # Sending confirmation email
            user_email = form.cleaned_data.get('email')
            send_mail(
                subject='Thank You for Contacting Us!',
                message = f"Dear {form.cleaned_data.get('name')},\n\nThank you for reaching out. We have received your message and will get back to you shortly.\n\nBest regards,\nFruitables",
                from_email='jayvyas0802@gmail.com',  # Change this to your email or DEFAULT_FROM_EMAIL
                recipient_list=[user_email],
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully. Thank you for reaching out to us!')
            return redirect('contact')
    else:
        form = ContactForm()
        subscribe_form = SubscribeForm()
    return render(request, 'contact.html', {'form': form,'subscribe_form':subscribe_form})

def testimonial(request):
    reviews = Testimonial.objects.filter(rating__gt=3)[:6]
    return render(request , 'testimonial.html',{'reviews': reviews})

def error(request, exception=None):
    return render(request, '404.html', status=404)

def policy(request):
    return render(request , 'policy.html')

def terms(request):
    return render(request , 't&c.html')
   

def logout_view(request):
    logout(request)
    return redirect('index')

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')  # You can handle Toastify on the login page
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Welcome to fruitables! from farm to your family.')
            return redirect('index')  # Show Toastify on the index page or handle Toastify on login page
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def search_results(request):
    query = request.GET.get('q', '')
    products = Products.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'products': products, 'query': query})

def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Save the email to the Subscriber table
            Subscriber.objects.create(email=email)
            
            # Send a confirmation email to the user
            send_mail(
                subject='Thank you for subscribing!',
                message=f"Thank you for subscribing to our newsletter! We will keep you updated with the latest news and updates.\n\nRegards\nFruitables",
                from_email='your_email@example.com',  # Replace with your email
                recipient_list=[email],
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for subscribing! A confirmation email has been sent to your email address.')
            return redirect('subscribe')
    else:
        form = SubscribeForm()

    return redirect(request.META.get('HTTP_REFERER', 'index'))

def render_to_pdf(html_content):
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html_content.encode("UTF-8")), dest=result)
    if pdf.err:
        return None
    return result.getvalue()

# API 
class ProductListView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class BillingDetailView(generics.ListCreateAPIView):
    queryset = BillingDetail.objects.all()
    serializer_class = BillingSerializer
    
class BillingDetailListView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BillingDetail.objects.all()
    serializer_class = BillingSerializer
  

