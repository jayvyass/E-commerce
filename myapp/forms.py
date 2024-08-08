from django import forms
from .models import Contact , Testimonial

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
