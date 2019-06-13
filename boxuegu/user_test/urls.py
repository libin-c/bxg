from django.conf.urls import url,include
from . import views
urlpatterns = [
    url('^user_test/',views.UserRegisterView.as_view()),
]
