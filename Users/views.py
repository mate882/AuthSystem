from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = request.POST.get('email')

        # Check if email already used
        if User.objects.filter(email=email).exists():
            messages.error(request, "❌ Email already in use.")
            return render(request, 'main/register.html', {'form': form})

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"

            message = render_to_string('main/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            email_message = EmailMessage(mail_subject, message, to=[email])
            email_message.send()

            messages.success(request, "✅ Please confirm your email address to complete registration.")
            return redirect('register')

        else:
            messages.error(request, "❌ There is something wrong with your input.")
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})


from django.contrib.auth import login


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your account has been activated successfully!")
        return redirect('profile')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('register')

def profile(request):
    if not request.user.is_verified:
        messages.warning(request, "⚠️ Please verify your email to access the profile.")
        return redirect('profile')

    return render(request, 'main/profile.html', {'user': request.user})

def user_login(request):
    return render(request, 'main/login.html')