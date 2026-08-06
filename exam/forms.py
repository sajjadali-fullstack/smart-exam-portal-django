from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['name', 'email', 'rating', 'message']

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),

            'rating': forms.Select(
                choices=[
                    (5,'⭐⭐⭐⭐⭐ Excellent'),
                    (4,'⭐⭐⭐⭐ Very Good'),
                    (3,'⭐⭐⭐ Good'),
                    (2,'⭐⭐ Fair'),
                    (1,'⭐ Poor')
                ],
                attrs={'class':'form-select'}
            ),

            'message': forms.Textarea(attrs={
                'class':'form-control',
                'rows':5,
                'placeholder':'Share your experience...'
            }),

        }


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Choose a username"
        })

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your email address"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Create a strong password"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm your password"
        })

from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your username"
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter your password"
        })