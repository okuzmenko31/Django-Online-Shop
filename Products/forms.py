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


class OrderingChoices(forms.Form):
    ORDERING_CHOICES = [
        ('standard', 'Стандартна сортировка'),
        ('cheaper', 'Дешевше'),
        ('expensive', 'Дорожче'),
    ]

    ordering = forms.TypedChoiceField(label='Сортування', choices=ORDERING_CHOICES, required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
