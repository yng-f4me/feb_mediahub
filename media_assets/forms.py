from django import forms
from .models import MediaAssets

class MediaAssetsForm(forms.ModelForm):
    '''
    define our forms fields for media upload
    '''
    class Meta:
        model = MediaAssets
        fields = ['title', 'description', 'category', 'media_file', 'is_public']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
                }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
                }),
            'category': forms.Select(attrs={
                'class': 'form-control'
                }),
                'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
                }),
        }