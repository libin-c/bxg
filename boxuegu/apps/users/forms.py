
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

class LoginForm(forms.Form):
    """
        登录表单
    """

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    """
        注册表单
    """

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误！'})


class ForgetForm(forms.Form):
    """
        忘记密码表单
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误！'})


class ModifyPwdForm(forms.Form):
    """
        验证两次密码表单
    """
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    """
        上传图片验证表单
    """
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    """
        用户表单
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']