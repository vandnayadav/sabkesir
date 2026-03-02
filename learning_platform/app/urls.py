from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('about/',views.about,name="about") ,
    path('course/',views.courses,name="course"),
    path('contact/',views.contact,name="contact"),
    path('add-to-cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name="cart"),
     path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
]
=======
    path('about/', views.about, name="about"),
    path('course/', views.courses, name="course"),
    path('contact/', views.contact, name="contact"),
>>>>>>> 6b4c67d75938b77a5b31fcd3da2233ab642e9eac

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]