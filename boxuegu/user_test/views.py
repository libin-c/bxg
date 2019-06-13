from django.shortcuts import render
from django.views import View
from user_test.form import RegisterForm
from django.http import HttpResponse


# Create your views here.


class UserRegisterView(View):
    """
        用户注册
    """

    def get(self, request):
        """
            获取注册页面
        :param request:
        :return:
        """

        # 生成表单对象
        register_form = RegisterForm()

        return render(request, 'register_test.html', {'register_form': register_form})

    def post(self, request):
        """
            保存用户注册数据
        :param request:
        :return:
        """
        # 获取表单数据
        data = request.POST
        # 生成表单对象
        register_form = RegisterForm(data)
        # 验证表单
        res = register_form.is_valid()
        # 可以通过error属性获取验证失败的原因
        error=register_form.errors
        if res:
            # 验证成功则保存数据
            return HttpResponse('ok')
        # 验证失败返回表单对象，在模板中渲染错误原因
        return render(request, 'register_test.html', {'register_form': register_form})
