from django.urls import path
from . import views

app_name = 'app'  # ✅ Fixed — matches your apps.py where name = 'app'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('course/', views.courses, name='course'),
    path('contact/', views.contact, name='contact'),

    # Cart
    path('add_to_cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    # ✅ Live Classes — separate pages, not index
    path('live-classes/', views.live_classes_home, name='live_classes_home'),
    path('live-classes/<int:pk>/', views.live_class_detail, name='live_class_detail'),
    path('live-classes/api/live-status/', views.api_live_status, name='api_live_status'),
]