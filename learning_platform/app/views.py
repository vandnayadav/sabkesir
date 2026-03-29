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
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.conf import settings
import ssl
import certifi
import re




# ---------- NORMAL PAGES ----------
def index(request):
    return render(request, "index.html")

def about(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"""
        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER,
            ['projectclient26@gmail.com'],
        )

        messages.success(request, "Message sent successfully")

    return render(request, "about.html")

def contact(request):
    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"""
Name: {name}
Email: {email}

Message:
{message}
        """

        # SSL Fix for Python 3.14
        import ssl
        import smtplib
        from email.mime.text import MIMEText

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        msg = MIMEText(full_message)
        msg['Subject'] = subject or "Contact Form Query"
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = 'projectclient26@gmail.com'

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, ['projectclient26@gmail.com'], msg.as_string())

        messages.success(request, "Message sent successfully!")

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


#import re  # ← file ke top mein add karo

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        contact = request.POST.get('contact', '').strip()

        # Validations
        if not name or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('app:signup')

        # ✅ Name validation — sirf letters aur spaces
        if not re.match(r'^[A-Za-z\s]+$', name):
            messages.error(request, "Name mein sirf letters allowed hain, numbers nahi!")
            return redirect('app:signup')

        # ✅ Password length — kam se kam 8 characters
        if len(password) < 8:
            messages.error(request, "Password kam se kam 8 characters ka hona chahiye!")
            return redirect('app:signup')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('app:signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists")
            return redirect('app:signup')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        login(request, user)
        next_url = request.POST.get('next')
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

            domain = request.get_host()
            link = f"http://{domain}/reset/{uid}/{token}/"

            # SSL Fix for Python 3.14 on Windows
            import ssl
            import smtplib
            from email.mime.text import MIMEText

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            msg = MIMEText(f"Click this link to reset password: {link}")
            msg['Subject'] = "Password Reset"
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = email

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.ehlo()
                server.starttls(context=context)
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(settings.EMAIL_HOST_USER, [email], msg.as_string())

            messages.success(request, "Reset link sent to email")

        else:
            messages.error(request, "Email not found")

    return render(request, "forgot_password.html")

# ---------- RESET PASSWORD ----------
def reset_password(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        if request.method == "POST":
            password = request.POST['password']
            user.set_password(password)
            user.save()

            messages.success(request, "Password changed successfully")
            return redirect('app:login')

        return render(request, "reset_password.html")

    else:
        messages.error(request, "Invalid or expired link")
        return redirect('app:login')

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