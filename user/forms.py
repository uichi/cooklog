from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm
)
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        max_length=16,
        label='ユーザー名',
        required=True
    )
    email = forms.CharField(
        max_length=256,
        label='メールアドレス',
        required=True
    )
    password1 = forms.CharField(
        label='パスワード',
        required=True,
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='パスワード(確認用)',
        required=True,
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AccountSettingsForm(forms.ModelForm):
    image = forms.ImageField(
        label='プロフィール画像',
        required=False,
        widget=forms.FileInput(attrs={'id': 'inputFile', 'class': 'custom-file-input'})
    )
    username = forms.CharField(
        label='ユーザー名',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        label='メールアドレス',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    introduction = forms.CharField(
        label='自己紹介',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('image', 'username', 'email', 'introduction')


class LoginForm(AuthenticationForm):
    password = forms.CharField(
        label='パスワード',
        required=True,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
