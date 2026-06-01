from django import forms
from .models import Post
 
 
class CreatePostForm(forms.ModelForm):
    '''A form to add an Article to the database.'''
 
    class Meta:
        image_file = forms.ImageField(required=False)
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']