from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .forms import *
from .models import *

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.widgets.EmailInput(attrs={"class": "form-control"}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'

class UserProfileForm(forms.ModelForm):
    YEARS = [x for x in range(1940, 2021)]
    BirthDate = forms.DateField(widget=forms.widgets.DateTimeInput(attrs={"type": "date","class":"form-control"}))
    class Meta:
        model = UserProfile
        fields = ('BirthDate',)

class EditProfileForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ['username','birthdate','favorite_category', 'profile_picture']

class UpdateProfilePicture(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': 50, 'rows': 4}))
