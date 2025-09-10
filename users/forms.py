
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django_flatpickr.widgets import DateTimePickerInput
from hashlib import md5




class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }




class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username or Email'}),
        label="Username or Email")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField()
    # avatar = forms.ImageField(disabled=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'description', 'birthdate']
        widgets = {
            'birthdate': DateTimePickerInput()}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance and self.instance.pk:
    #         self.fields['avatar'].initial = self.instance.make_avatar(128)




    class Media:
        css = {
            'all': ['/static/styles/form_style.css']
        }