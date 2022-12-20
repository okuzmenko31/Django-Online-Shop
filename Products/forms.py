from django import forms
from .models import Reviews


class ReviewsForms(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['name', 'review', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ваше ім'я"}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': "Ваш відгук"}),
        }
