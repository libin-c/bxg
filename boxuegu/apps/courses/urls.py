from django.conf.urls import url, include
from . import views

urlpatterns = [
    # 注册
    url(r'^course_list/$', views.CourseListView.as_view(), name='course_list'),


]
