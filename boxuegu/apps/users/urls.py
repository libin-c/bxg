from django.conf.urls import url, include
from . import views

urlpatterns = [
    # 注册
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 登录
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    # 忘记密码 url'forget_pwd
    url(r'^forget/$', views.ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/$', views.ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', views.ResetView.as_view(), name='reset_pwd'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^image/upload/$', views.UploadImageView.as_view(), name='image_upload'),
    # users/info/
    url(r'^user_info/$', views.InfoView.as_view(), name='user_info'),
    url(r'^users/info/$', views.InfoView.as_view(), name='user_info'),
    # mymessage
    url(r'^mymessage/$', views.MyMessageView.as_view(), name='mymessage'),
    # myfav_org
    url(r'^myfav_org/$', views.MyFavOrgView.as_view(), name='myfav_org'),
    url(r'^myfav_teacher/$', views.MyFavTeacherView.as_view(), name='myfav_teacher'),
    url(r'^myfav_course/$', views.MyFavCourseView.as_view(), name='myfav_course'),
    # mycourse
    url(r'^mycourse/$', views.MyCourseView.as_view(), name='mycourse'),

]
