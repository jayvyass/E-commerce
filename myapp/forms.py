from django import forms
from .models import Contact , Testimonial , BillingDetail
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-100 form-control border-0 py-3 mb-4',
                'placeholder': 'Your Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-100 form-control border-0 py-3 mb-4',
                'placeholder': 'Enter Your Email',
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-100 form-control border-0 mb-4',
                'rows': 5,
                'style': 'resize: none; width: 100%; height: 180px;',
                'placeholder': 'Your Message',
            }),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'email', 'review', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control border-0 me-4',
                'placeholder': 'Your Name '
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-0',
                'placeholder': 'Your Email '
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control border-0',
                'cols': 30,
                'rows': 8,
                'placeholder': 'Your Review ',
                'spellcheck': 'false'
            }),
            'rating': forms.HiddenInput(attrs={'id': 'rating', 'value': '0'}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError('Passwords do not match')

        return cleaned_data

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class BillingDetailForm(forms.ModelForm):
    class Meta:
        model = BillingDetail
        fields = [
            'first_name',
            'last_name',
            'address',
            'town_city',
            'country',
            'postcode_zip',
            'mobile',
            'email',
            'order_notes',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control my-3',
              
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control my-3',
               
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control my-3',
              
            }),
            'town_city': forms.TextInput(attrs={
                'class': 'form-control my-3',
                
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control my-3',
              
            }),
            'postcode_zip': forms.TextInput(attrs={
                'class': 'form-control my-3',
                
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control my-3',
                'type': 'tel',
               
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control my-3',
               
            }),
            'order_notes': forms.Textarea(attrs={
                'class': 'form-control my-3',
                'cols': 30,
                'rows': 11,
              
                'spellcheck': 'false',
            }),
        }