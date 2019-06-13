from django import forms
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    """
        注册表单
    """
    email=forms.CharField(required=True)  # 邮箱字段
    password=forms.CharField(required=True,min_length=5) # 密码字段
    captcha=CaptchaField(error_messages={'invalid':'验证码错误'})  # 验证码字段
