from django.shortcuts import render
from .models import Course


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")




def courses(request):
    courses = Course.objects.all()
    return render(request, "course.html", {'courses': courses})

def course_detail(request, id):
    course = Course.objects.get(id=id)
    return render(request, "course_detail.html", {"course": course})