from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from courses.models import Course
from organization.models import CourseOrg
from users.models import Banner


class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all()
        courses = Course.objects.all()
        banner_courses = Course.objects.all()
        course_orgs = CourseOrg.objects.all()
        context = {

            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,

        }

        return render(request,'index.html',context)
