import redis
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from apps.users.forms import LoginForm, CaptchaForm, DynamicLoginPostForm, RegisterPostForm
from apps.users.models import UserProfile
from mysite.settings import default_code, fake_password


# Create your views here.

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        captcha_form = CaptchaForm()
        return render(request, "register.html", {
            "captcha_form": captcha_form
        })

    def post(self, request, *args, **kwargs):
        d_post_form = RegisterPostForm(request.POST)
        if d_post_form.is_valid():
            mobile = d_post_form.cleaned_data["mobile"]
            password = d_post_form.cleaned_data["password"]
            users = UserProfile.objects.filter(mobile=mobile)
            if users:
                msg = "该账户已注册！"
                dynamic_captcha_form = CaptchaForm()
                return render(request, "register.html", {
                    "dynamic_captcha_form": dynamic_captcha_form,
                    "msg": msg
                })
            else:
                user = UserProfile(username=mobile)
                user.mobile = mobile
                user.set_password(password)
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        else:
            dynamic_captcha_form = CaptchaForm()
            return render(request, "register.html", {
                "d_post_form":d_post_form,
                "dynamic_captcha_form": dynamic_captcha_form
            })



class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        dynamic_captcha_form = CaptchaForm()
        return render(request, "login.html", {
            "dynamic_captcha_form": dynamic_captcha_form
        })

    def post(self, request, *args, **kwargs):
        d_post_form = DynamicLoginPostForm(request.POST)
        if d_post_form.is_valid():
            mobile = d_post_form.cleaned_data["mobile"]
            users = UserProfile.objects.filter(mobile=mobile)
            if users:
                user = users[0]
            else:
                user = UserProfile(username=mobile)
                password = fake_password
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            dynamic_captcha_form = CaptchaForm()
            return render(request, 'login.html', {
                "d_post_form": d_post_form,
                "dynamic_captcha_form": dynamic_captcha_form
            })


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        d_form = CaptchaForm(request.POST)
        re_dict = {}
        if d_form.is_valid():
            mobile = d_form.cleaned_data["mobile"]
            code = default_code
            send_sms_func_res = True
            if send_sms_func_res:
                re_dict["status"] = "success"
                r = redis.Redis(host="127.0.0.1", port=6379, charset="utf8", decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 30)
            else:
                re_dict["status"] = "fail"
                re_dict["msg"] = "发送验证码失败"
        else:
            for key, value in d_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        captcha_form = CaptchaForm()
        return render(request, "login.html", {
            "captcha_form": captcha_form,
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误", 'login_form': login_form})
        else:
            return render(request, 'login.html', {"login_form": login_form})
