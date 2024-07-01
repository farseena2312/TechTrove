from django import forms
from .models import Product, UserProfile
from user_account.models import UserAccount
from . models import ReviewRating


class UserForm(forms.ModelForm):
    class Meta:
        model=UserAccount
        fields=['first_name', 'last_name', 'email','phone_number']


class ReviewForm(forms.ModelForm):
    class Meta:
        model=ReviewRating
        fields=['subject','review','rating']        



class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['gender','profile_picture','date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }