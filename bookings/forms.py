from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Booking

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                self.fields[field_name].widget.attrs['placeholder'] = 'Choose a username'
            elif field_name == 'password1':
                self.fields[field_name].widget.attrs['placeholder'] = 'Enter your password'
            elif field_name == 'password2':
                self.fields[field_name].widget.attrs['placeholder'] = 'Confirm your password'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'rows': 3
            })
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']
        widgets = {
            'number_of_seats': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of seats'
            })
        }
    
    def __init__(self, *args, travel_option=None, **kwargs):
        self.travel_option = travel_option
        super().__init__(*args, **kwargs)
        
    def clean_number_of_seats(self):
        seats = self.cleaned_data['number_of_seats']
        if not self.travel_option:
            raise forms.ValidationError("Travel option not specified.")
            
        if seats < 1:
            raise forms.ValidationError("Number of seats must be at least 1.")
            
        if seats > self.travel_option.available_seats:
            raise forms.ValidationError(f"Only {self.travel_option.available_seats} seats available.")
            raise forms.ValidationError(f"Only {travel_option.available_seats} seats available.")
        if seats < 1:
            raise forms.ValidationError("Number of seats must be at least 1.")
            
        return seats
