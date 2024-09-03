from django import forms
from .models import Contact , Testimonial , BillingDetail ,Subscriber , Category1 , Category2 , Products
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
            'name': forms.TextInput(attrs={'class': 'form-control border-0 me-4', 'placeholder': 'Your Name '}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-0', 'placeholder': 'Your Email '}),
            'review': forms.Textarea(attrs={'class': 'form-control border-0', 'cols': 30, 'rows': 8, 'placeholder': 'Your Review ', 'spellcheck': 'false'}),
            'rating': forms.HiddenInput(attrs={'id': 'rating', 'value': '0'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating or rating == '0':
            raise forms.ValidationError('Please select a rating.')
        return rating


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password'
    )

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border-0 ',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control border-0 ',}))


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
                'rows': 8,
              
                'spellcheck': 'false',
            }),
        }

class SubscribeForm(forms.Form):
    model = Subscriber
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control border-0 py-3 px-3 rounded-pill',
            'placeholder': 'Your Email'
        }),
        required=True,
    )


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