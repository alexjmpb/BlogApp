from django import forms
from blog.models import UserBlog
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MinLengthValidator, EmailValidator
from django.contrib.auth.password_validation import *
from django.contrib.auth import authenticate
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

allowed_username_characters = 'abcdefghijklmnopqrstuvwxyz.0123456789_-'

class UserBaseForm(forms.Form):
    username = forms.CharField(label=_('Username'), validators=[MinLengthValidator(3, message=_("Your username must have at least 3 characters"))])
    email = forms.EmailField(label=_('Email'), validators=[EmailValidator(message=_("Please enter a valid email"))])

    def clean_username(self):
        username = self.cleaned_data.get('username')

        for letter in username:
            if not letter.lower() in allowed_username_characters:
                raise ValidationError(_("Your username cannot contain special character such as: \" ' / * + - [ ] { } or others"))


        if len(list(UserBlog.objects.filter(username__iexact=username))):
            if not self.instance.username.lower() == username.lower():
                raise ValidationError(_("This username is already taken"))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if len(list(UserBlog.objects.filter(email__iexact=email))):
            if not self.instance.email.lower() == email.lower():
                raise ValidationError(_("This email is already taken"))
        return email


class UpdateUserInfo(UserBaseForm, forms.ModelForm):
    class Meta:
        model = UserBlog
        fields = ('username', 'email', 'description',)
    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
        return user

class UserImageForm(forms.ModelForm):
    user_image = forms.ImageField(widget=forms.FileInput(attrs={'onchange' : "previewFile()"}), required=False, label=_("Your image"))
    class Meta:
        model = UserBlog
        fields = ('user_image',)

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
        return user

class CreateUserForm(forms.ModelForm, UserBaseForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)
    

    class Meta:
        model = UserBlog
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password2 != password1:
            raise ValidationError(_("Passwords don't match"))
        return password2

    def clean_password1(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password1 = cleaned_data.get("password1")
        password_validators_help_texts()
        validate_password(password1)

        if password1:
            has_upper = False
            for letter in password1:
                if letter.isupper():
                    has_upper = True
            if not has_upper:
                raise ValidationError(_("Your password must contain at least one uppercase letter"))
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user
