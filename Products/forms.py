from django import forms
from .models import Reviews


class ReviewsForms(forms.ModelForm):
    """Form for posting reviews"""

    class Meta:
        model = Reviews
        fields = ['name', 'review', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Your name"}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': "Review"}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0:
            self.add_error('rating', 'Your posted rating must be more than 0!')
        return rating


class OrderingChoicesForm(forms.Form):
    """Form to for select ordering choices"""
    ORDERING_CHOICES = [
        ('standard', 'Standard sorting'),
        ('cheaper', 'Cheaper'),
        ('expensive', 'Expensive'),
    ]
    ordering = forms.TypedChoiceField(label='Sorting', choices=ORDERING_CHOICES, required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
