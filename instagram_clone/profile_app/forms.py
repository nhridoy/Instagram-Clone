from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, AuthenticationForm
from profile_app.models import UserDetails


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='',
                             widget=forms.EmailInput(attrs={'class': 'text-input', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, label='',
                                 widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': 'Full Name'}))
    username = forms.CharField(required=True, label='',
                               widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': 'Username'}))
    password1 = forms.CharField(required=True, label='',
                                widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, label='', widget=forms.PasswordInput(
        attrs={'class': 'text-input', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label='',
                               widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': 'Username'}))
    password = forms.CharField(required=True, label='',
                               widget=forms.PasswordInput(attrs={'class': 'text-input', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = '__all__'


class ChangeProfilePicForm(forms.ModelForm):
    # profile_pic = forms.ImageField(
    #     widget=forms.TextInput(attrs={'type': 'file', 'accept': 'image/*', 'class': 'text-input'}))

    class Meta:
        model = UserDetails
        fields = ('profile_pic',)


class EditProfileForm(forms.ModelForm):
    dob = forms.DateField(label='Date of Birth',
                          widget=forms.TextInput(attrs={'type': 'date', 'class': 'text-input'}))
    about_user = forms.Field(required=False,
                             widget=forms.Textarea(attrs={'class': 'text-input', 'style': 'resize:none'}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'text-input'}))
    facebook = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'text-input'}))

    class Meta:
        model = UserDetails
        exclude = ('user', 'profile_pic',)


class EditBasicForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'text-input'}))

    class Meta:
        model = User
        fields = ('first_name',)
