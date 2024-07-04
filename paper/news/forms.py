from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class CreatePost(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'text', 'image', 'category']
        widgets = {
            'title': forms.Textarea(attrs={'cols':80, 'rows': 2}),
            'text': forms.Textarea(attrs={'cols':100, 'rows':6}),
        }
    

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image')


class EditUserForm(UserChangeForm):
    class Meta:
        models = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image')

class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'cols':80, 'rows': 2}),
        }