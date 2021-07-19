from django import forms
from .models import Contact, Message
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class Contact_form(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('contact_first_name', 'contact_last_name', 'contact_mobile_number', 'contact_email')


class Message_form(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        widget = {
            'message_created_by': forms.TextInput(attrs={'value': '', 'id': 'message_id'}),
        }


class SignUpForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class EditprofileForm(UserChangeForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    username = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class statusForm(UserChangeForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    username = forms.CharField()
    is_active = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
