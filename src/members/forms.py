from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from familypost.models import UserProfile

# ClearableFileInput Template
from django.forms.widgets import ClearableFileInput, CheckboxInput
#from django.contrib.auth.views import PasswordChangeForm

class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(label='New Password', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(label='New Password Confirmation', max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class SignUpForm(UserCreationForm):
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    ### Auto create user profile
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        profile, created = UserProfile.objects.update_or_create(user=user)
        profile.first_name = self.cleaned_data["first_name"]
        profile.last_name = self.cleaned_data["last_name"]
        profile.email = self.cleaned_data["email"]
        profile.save()
        return user

#class EditProfileForm(UserChangeForm):
class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    #password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'hidden'}))

    class Meta:
        model = User
        fields = ( 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff')
    


class MyImageWidget(ClearableFileInput):
    template_name = "registration/customizeFile.html"

class EditUserProfileForm(forms.ModelForm):

    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}))
    profile_image = forms.ImageField(required=False, widget=MyImageWidget(attrs={'class':'form-control'}))
    
    www_url = forms.CharField(max_length=100, required=False , widget=forms.TextInput(attrs={'class':'form-control'}))
    ig_url = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model = UserProfile
        fields = ('profile_image', 'first_name', 'last_name', 'email', 'bio', 'www_url','ig_url')

