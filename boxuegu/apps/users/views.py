import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from pymysql import DatabaseError
from django.http.response import HttpResponse, JsonResponse

from courses.models import Course
from operation.models import UserMessage, UserFavorite, UserCourse
from organization.models import CourseOrg, Teacher
from users import constants
from users.forms import RegisterForm, LoginForm, ForgetForm, ModifyPwdForm, UserInfoForm, UploadImageForm
from users.models import UserProfile, Banner
from users.utils import SecretOauth


class RegisterView(View):
    def get(self, request):
        """
            获取注册页面
        :param request:
        :return:
        """
        # 生成表单对象
        register_form = RegisterForm()
        # 调用模版渲染生成表单
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        """
            验证表单数据
        :param request:
        :return:
        """
        # 1、获取前端传递的表单数据
        data = request.POST

        # 2、验证表单数据
        register_form = RegisterForm(data)
        res = register_form.is_valid()  # 验证成功返回True，验证失败返回False

        if res:
            # 验证成功，则执行相应业务逻辑操作，这里就直接返回验证成功后的字段数据
            # 获取验证成功后的字段
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']

            try:
                UserProfile.objects.get(username=email)
            except Exception as e:
                # 2.1 用户名
                if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                    return render(request, 'register.html', {'register_form.errors': {"error": '用户名 格式不正确'}})
                # 2.2 密码
                if not re.match(r'^[0-9A-Za-z]{6,20}$', password):
                    return render(request, 'register.html', {'register_form.errors': {"error": '密码 格式不正确'}})

                user = UserProfile.objects.create(
                    username=email,
                    email=email,
                    password=password
                )
                login(request, user)
                response = redirect(reverse('index'))
                response.set_cookie('username', user.username, constants.USERNAME_EXPIRE_TIME)
                return response
            register_error = {"error": '注册账号重复 '}
            return render(request, 'register.html', {'register_errors': register_error})
            # response = redirect(reverse('register'))

        # 验证失败，则在注册模板中通过register_form.errors获取错误
        return render(request, 'register.html', {'register_form': register_form})


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'register_form': login_form})

    def post(self, request):
        """
                    验证表单数据
                :param request:
                :return:
                """
        # 1、获取前端传递的表单数据
        data = request.POST
        # 2、验证表单数据
        login_form = LoginForm(data)
        res = login_form.is_valid()  # 验证成功返回True，验证失败返回False
        if res:
            # 验证成功，则执行相应业务逻辑操作，这里就直接返回验证成功后的字段数据
            # 获取验证成功后的字段
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login_error = {"error": '用户名或者密码错误 验证失败'}
            if user == None:

                return render(request, 'login.html', {'form_errors': login_error})
            else:
                login(request, user)
                response = redirect(reverse('index'))
                response.set_cookie('username', username, constants.USERNAME_EXPIRE_TIME)
                return response
        # 验证失败，则在登录模板中通过register_form.errors获取错误
        return render(request, 'login.html', {'login_form': login_form})


class ForgetPwdView(View):
    def get(self, request):
        """
            获取注册页面
        :param request:
        :return:
        """
        # 生成表单对象
        forget_form = ForgetForm()
        # 调用模版渲染生成表单
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        data = request.POST
        # 2、验证表单数据
        forget_form = ForgetForm(data)
        res = forget_form.is_valid()  # 验证成功返回True，验证失败返回False

        if res:

            # 验证成功，则执行相应业务逻辑操作，这里就直接返回验证成功后的字段数据
            # 获取验证成功后的字段
            email = forget_form.cleaned_data['email']
            try:
                user = UserProfile.objects.get(
                    username=email,
                )
            except Exception as e:
                return render(request, 'forgetpwd.html', {'forget_errors': {"error": ' 用户不存在'}})
            from django.core.mail import send_mail
            # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
            send_mail(subject='博学谷密码重置', message='', from_email=settings.EMAIL_FROM,
                      recipient_list=[email],
                      html_message='请点击你的链接重置你的密码<p><a href="%s">%s<a></p>' % (
                          'http://127.0.0.1:8000/reset/' + SecretOauth().dumps(email),
                          'http://127.0.0.1:8000/reset/' + SecretOauth().dumps(email)),
                      fail_silently=False)
            return render(request, 'send_success.html')
        # 验证失败，则在注册模板中通过register_form.errors获取错误
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        email = SecretOauth().loads(active_code)
        try:
            user = UserProfile.objects.get(username=email)
        except Exception as e:
            return render(request, 'password_reset.html', {'modify_form': {'error': '验证的用户不存在'}})
        # 调用模版渲染生成表单
        return render(request, 'password_reset.html', {'email': email})

    def post(self, request, active_code):
        email = SecretOauth().loads(active_code)
        data = request.POST

        # 2、验证表单数据
        modify_form = ModifyPwdForm(data)
        res = modify_form.is_valid()  # 验证成功返回True，验证失败返回False
        if res:
            password1 = modify_form.cleaned_data['password1']
            password2 = modify_form.cleaned_data['password2']

            if password1 == password2:
                try:
                    user = UserProfile.objects.get(username=email)
                except Exception as e:
                    return render(request, 'password_reset.html', {'modify_errors': {'error': '用户不存在'}, 'email': email})
                if user.check_password(password1) == True:
                    return render(request, 'password_reset.html',
                                  {'modify_errors': {'error': '新密码和旧密码重复'}, 'email': email})
                else:
                    user.set_password(password1)
                    user.save()
                    login(request, user)
                    response = redirect(reverse('index'))
                    response.set_cookie('username', email, constants.USERNAME_EXPIRE_TIME)
                    return response
            else:
                return render(request, 'password_reset.html', {'modify_errors': {'error': '修改密码失败'}})

        return render(request, 'password_reset.html', {'modify_form': modify_form})


class ModifyPwdView(View):
    def post(self, request):
        email = request.POST.get('email')
        print(email)
        data = request.POST

        # 2、验证表单数据
        modify_form = ModifyPwdForm(data)
        res = modify_form.is_valid()  # 验证成功返回True，验证失败返回False
        if res:
            password1 = modify_form.cleaned_data['password1']
            password2 = modify_form.cleaned_data['password2']

            if password1 == password2:
                try:
                    user = UserProfile.objects.get(username=email)
                except Exception as e:
                    return render(request, 'password_reset.html', {'modify_errors': {'error': '用户不存在'}, 'email': email})
                if user.check_password(password1) == True:
                    return render(request, 'password_reset.html',
                                  {'modify_errors': {'error': '新密码和旧密码重复'}, 'email': email})
                else:
                    user.set_password(password1)
                    user.save()
                    login(request, user)
                    response = redirect(reverse('index'))
                    response.set_cookie('username', email, constants.USERNAME_EXPIRE_TIME)
                    return response
            else:
                return render(request, 'password_reset.html', {'modify_errors': {'error': '修改密码失败'}})

        return render(request, 'password_reset.html', {'modify_form': modify_form})


class LogoutView(View):
    def get(self, request):
        # 清理session
        logout(request)
        response = redirect(reverse('login'))
        response.delete_cookie('username')
        return response


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        data = request.POST
        image_form = UploadImageForm(data, request.FILES, instance=request.user)
        res = image_form.is_valid()

        if res:
            request.user.save()
            return JsonResponse({"status": "success", "msg": "头像修改成功"})
        return JsonResponse({
            "status": "success",
            "msg": '头像修改失败'
        })


class InfoView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.COOKIES['username']
        return render(request, 'usercenter-info.html', {'MEDIA_URL': settings.MEDIA_URL, 'email': SecretOauth().dumps(username)})

    # def post(self, request):
    #
    #     username = request.COOKIES['username']
    #     user = UserProfile.objects.get(username=username)
    #     data =request.POST
    #     user_info_form=UserInfoForm(data)
    #
    #
    #     if user_info_form.is_valid():
    #     # 2、验证表单数据
    #         if user_info_form.errors['birthday']:
    #             nick_name = user_info_form.cleaned_data['nick_name']
    #             gender = user_info_form.cleaned_data['gender']
    #             address = user_info_form.cleaned_data['address']
    #             mobile = user_info_form.cleaned_data['mobile']
    #             birthday = data.get('birthday')
    #             today_date = datetime.strptime(birthday, '%Y年%m月%d日')
    #             user.nick_name = nick_name
    #             user.gender = gender
    #             user.address = address
    #             user.birthday = today_date
    #             user.mobile = mobile
    #             user.save()
    #             context = {
    #                 "status": "success"
    #             }
    #             return JsonResponse(context)
    #         else:
    #             nick_name = user_info_form.cleaned_data['nick_name']
    #             gender = user_info_form.cleaned_data['gender']
    #             address = user_info_form.cleaned_data['address']
    #             mobile = user_info_form.cleaned_data['mobile']
    #             birthday =user_info_form.cleaned_data['birthday']
    #             user.nick_name = nick_name
    #             user.gender = gender
    #             user.address = address
    #             user.birthday = birthday
    #             user.mobile = mobile
    #             user.save()
    #             context = {
    #                 "status": "success"
    #             }
    #             return JsonResponse(context)
    #     return  JsonResponse({
    #     "status": "error"
    #     })

    def post(self, request):
        data = request.POST
        user_form = UserInfoForm(data, instance=request.user)
        res = user_form.is_valid()
        if res:
            request.user.save()
            return redirect('users/info/')
        return render(request, 'usercenter-info.html', {'MEDIA_URL': settings.MEDIA_URL,
                                                        'status': '修改失败'})


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses,
            'MEDIA_URL': settings.MEDIA_URL
        })


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        data = UserFavorite.objects.filter(fav_type=3, user=user.id, )
        org_list = [CourseOrg.objects.get(id=i.fav_id) for i in data]
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'MEDIA_URL': settings.MEDIA_URL
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        data = UserFavorite.objects.filter(fav_type=3, user=user.id, )
        teacher_list = [Teacher.objects.get(id=i.fav_id) for i in data]
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'MEDIA_URL': settings.MEDIA_URL
        })


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        data = UserFavorite.objects.filter(fav_type=1, user=user.id, )
        course_id = [Course.objects.get(id=i.fav_id) for i in data]
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_id,
            'MEDIA_URL': settings.MEDIA_URL
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        messages = UserMessage.objects.filter(user=request.user.id)
        paginator = Paginator(messages, 10)
        page_mun = request.GET.get('page', 1)
        messages = paginator.page(page_mun)

        return render(request, 'usercenter-message.html', {
            'messages': messages,
        })


