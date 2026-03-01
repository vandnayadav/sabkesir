from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name="about") ,
    path('course/',views.courses,name="course"),
    path('contact/',views.contact,name="contact"),
    path('course/<int:id>/', views.course_detail, name="course_detail"),
]

