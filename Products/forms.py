from django import forms
from .models import Reviews


class ReviewsForms(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['name', 'review', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your name"}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': "Review"}),
        }


class OrderingChoices(forms.Form):
    ORDERING_CHOICES = [
        ('standard', 'Standard sorting'),
        ('cheaper', 'Cheaper'),
        ('expensive', 'Expensive'),
    ]

    ordering = forms.TypedChoiceField(label='Sorting', choices=ORDERING_CHOICES, required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
