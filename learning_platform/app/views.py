from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Cart
from django.shortcuts import render, redirect
from .models import Course
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from .models import LiveClass, RecordedReplay
from django.contrib.auth.decorators import login_required


# ---------- NORMAL PAGES ----------
def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")




@login_required(login_url='app:login')
def courses(request):
    courses = Course.objects.all()
    return render(request, "course.html", {'courses': courses})
   




# ADD TO CART
@login_required
def add_to_cart(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    # ⭐ check already exists
    cart_item = Cart.objects.filter(
        user=request.user,
        course=course
    ).first()

    if cart_item:
        # already added → go to cart page
        return redirect('app:cart')

    # add new item
    Cart.objects.create(
        user=request.user,
        course=course
    )

    return redirect('app:cart')


# CART PAGE
@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = sum(int(item.course.price) for item in cart_items)

    context = {
        'courses': [item.course for item in cart_items],
        'total': total
    }

    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, id):

    course = get_object_or_404(Course, id=id)

    Cart.objects.filter(
        user=request.user,
        course=course
    ).delete()

    return redirect('app:cart')


# ---------- SIGNUP ----------
def signup_view(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        next_url = request.POST.get('next')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect('app:signup')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        login(request, user)
        if next_url:
            return redirect(next_url)
        return redirect('app:index')

    return render(request, 'signup.html')


# ---------- LOGIN ----------
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        next_url = request.POST.get('next')

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('app:index')
        else:
            messages.error(request, "Invalid email or password. If you are new please signup.")
            return redirect('app:login')

    return render(request, 'login.html')


# ---------- LOGOUT ----------
def logout_view(request):
    logout(request)
    return redirect('app:login')


# ---------- FORGOT PASSWORD ----------
def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            link = f"http://127.0.0.1:8000/reset/{uid}/{token}/"

            send_mail(
                "Password Reset",
                f"Click this link to reset password: {link}",
                "admin@example.com",
                [email],
            )

            messages.success(request, "Reset link sent to email")

        else:
            messages.error(request, "Email not found")

    return render(request, "forgot_password.html")


# ---------- RESET PASSWORD ----------
def reset_password(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)

    if request.method == "POST":
        password = request.POST['password']
        user.set_password(password)
        user.save()
        return redirect('app:login')

    return render(request, "reset_password.html")

#Live class

# Make sure these exist at the bottom of your views.py

@login_required(login_url='app:login')
def live_classes_home(request):
    live_now = LiveClass.objects.filter(status='live').first()

    upcoming = LiveClass.objects.filter(
        status='upcoming',
        scheduled_at__gte=timezone.now()
    ).order_by('scheduled_at')[:6]

    replays = RecordedReplay.objects.select_related('live_class').order_by('-recorded_at')[:6]

    context = {
        'live_now': live_now,
        'upcoming_classes': upcoming,
        'replays': replays,
    }

    return render(request, 'live_classes/home.html', context)


@login_required(login_url='app:login')
def live_class_detail(request, pk):
    live_class = get_object_or_404(LiveClass, pk=pk)
    replay = getattr(live_class, 'replay', None)

    embed_url = None
    chat_url = None
    youtube_watch_url = None

    if live_class.status == 'live':
        embed_url = live_class.youtube_live_embed_url
        chat_url = live_class.youtube_chat_url
        youtube_watch_url = live_class.youtube_live_watch_url
    elif live_class.status == 'ended' and replay:
        embed_url = replay.embed_url
        youtube_watch_url = replay.watch_url

    context = {
        'live_class': live_class,
        'replay': replay,
        'embed_url': embed_url,
        'chat_url': chat_url,
        'youtube_watch_url': youtube_watch_url,
    }
    return render(request, 'live_classes/detail.html', context)


def api_live_status(request):
    live_now = LiveClass.objects.filter(status='live').first()
    data = {
        'is_live': live_now is not None,
        'class_id': live_now.pk if live_now else None,
        'title': live_now.title if live_now else None,
    }
    return JsonResponse(data)