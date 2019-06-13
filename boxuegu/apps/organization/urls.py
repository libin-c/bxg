from django.conf.urls import url, include
from . import views

urlpatterns = [
    # 注册
    url(r'^org_list/$', views.OrgListView.as_view(), name='org_list'),
    # url'org:teacher_list
    url(r'^teacher_list/$', views.OrgListView.as_view(), name='teacher_list'),
    url(r'^org_home/$', views.OrgListView.as_view(), name='org_home'),
    url(r'^add_fav/$', views.OrgListView.as_view(), name='add_fav'),
    # url'org：add_fav
]
