# File: forms.py
from django import forms
from .models import Reader, Book, Comment, Review

class CreateReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['username', 'display_name', 'reader_image_url', 'bio_text']

class UpdateReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['display_name', 'reader_image_url', 'bio_text']

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'page_num', 'reply']
        widgets = {
            'reply': forms.HiddenInput(),
            'page_num': forms.HiddenInput(),
        }

class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'stars']
        widgets = {
            'stars': forms.NumberInput(attrs={
                'min': 0,
                'max': 10,
                'placeholder': '0-10',
            })
        }