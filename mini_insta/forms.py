from django import forms
from .models import Post, Profile
 
 
class CreatePostForm(forms.ModelForm):
    '''A form to add a Post to the database.'''
 
    class Meta:
        image_file = forms.ImageField(required=False)
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']

class UpdatePostForm(forms.ModelForm):
    '''A form to update a Post to the database.'''
 
    class Meta:
        image_file = forms.ImageField(required=False)
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a profile to the database.'''
 
    class Meta:
        '''associate this form with the Profile model.'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']
 
## write the UpdateArticleView