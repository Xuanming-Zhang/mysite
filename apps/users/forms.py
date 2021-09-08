import redis
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class CaptchaForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        code = self.data["code"]
        mobile = self.data["mobile"]

        r = redis.Redis(host="127.0.0.1", port=6379, charset="utf8", decode_responses=True)
        redis_code = r.get(mobile)
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return code


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True)

    def clean_code(self):
        code = self.data["code"]
        mobile = self.data["mobile"]

        r = redis.Redis(host="127.0.0.1", port=6379, charset="utf8", decode_responses=True)
        redis_code = r.get(mobile)
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return code
