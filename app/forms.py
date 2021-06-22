from django import forms
from .models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms import Textarea, TextInput, FileInput

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "username"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "abc@mail.ru"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Enter password"}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Confirm password"}))


    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        check = User.objects.filter(username=username).exists()
        if check:
            self.add_error(None, 'User already exists')
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        check = User.objects.filter(email=email).exists()
        if check:
            self.add_error(None, 'Email already exists')
        else:
            return email

    def clean(self):
        password = self.cleaned_data.get("password")
        repeat_password = self.cleaned_data.get("password_repeat")
        if password != repeat_password:
            self.add_error(None, 'Passwords does not math')
        return self.cleaned_data


    def save(self):
        user = User.objects.create_user(username=self.cleaned_data.get("username"),
                                   password=self.cleaned_data.get("password"),
                                   email=self.cleaned_data.get("email"),
                                   )
        Profile.objects.create(user=user)
        return user

class SettingsForm(forms.ModelForm):
    username = forms.CharField(required=False, widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'login'
            }),
        label='Login')
    email = forms.EmailField(required=False, widget=TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        label='Email')
    avatar = forms.ImageField(required=False, widget=FileInput(attrs={
                'class': 'form-control'
            }),
        label='Avatar')

    def clean_email(self):
        email = self.cleaned_data['email']
        check = User.objects.filter(email=email).exists()
        if email == '':
            return email
        elif check:
            self.add_error(None, 'Email already exists')
        else:
            return email

    def clean_username(self):
        username = self.cleaned_data['username']
        check = User.objects.filter(username=username).exists()
        if username == '':
            return username
        elif check:
            self.add_error(None, 'Username already exists')
        else:
            return username

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']

    def save(self, *args, **kwarg):
        user = super().save(*args, **kwarg)
        if self.cleaned_data['avatar']:
            user.profile.avatar = self.cleaned_data['avatar']
        user.profile.save()
        return user


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter your answer here"}), label="")

class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "How?"}))
    text = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "And why?", "rows": 8}))
    tags = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "SQL, C++"}))

    def save(self):
        tags = []
        for tag in self.cleaned_data["tags"].split(','):
            tags.append(tag.strip())
        tag_list = []
        for tag in tags:
            t = Tag.objects.filter(name=tag).first()
            if t is None:
                t = Tag.objects.create(name=tag)
            else:
                t.save()
            tag_list.append(t)
        return tag_list
