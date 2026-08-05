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