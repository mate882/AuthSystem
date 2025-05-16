from django.shortcuts import render
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, "❌ Email already in use.")
            return render(request, 'main/register.html', {'form': form})

        if form.is_valid():
            form.save()
        else:
            messages.error(request, "❌ There is something wrong with password")
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})