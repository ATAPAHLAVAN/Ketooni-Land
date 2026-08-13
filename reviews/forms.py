from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """فرم نوشتن نظر"""
    
    class Meta:
        model = Review
        fields = ('title', 'comment', 'rating')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان نظر',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'نظرتان را بنویسید...',
                'rows': 5,
            }),
            'rating': forms.RadioSelect(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'title': 'عنوان نظر',
            'comment': 'متن نظر',
            'rating': 'امتیاز',
        }