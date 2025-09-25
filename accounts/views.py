from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import EmailForm, VerifyForm
from .models import OneTimeCode

def login_request_code(request):
    """Шаг 1: пользователь вводит e-mail, мы генерируем код и отправляем письмо"""
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            user, _ = User.objects.get_or_create(username=email, defaults={'email': email})
            otp = OneTimeCode.issue_for(user)
            send_mail(
                subject='Ваш код входа',
                message=f'Код для входа: {otp.code} (действует 10 минут).',
                from_email=None,
                recipient_list=[email],
                fail_silently=True
            )
            messages.success(request, 'Код отправлен на вашу почту.')
            return redirect(reverse('accounts:verify') + f'?email={email}')
    else:
        form = EmailForm(initial={'email': request.GET.get('email', '')})
    return render(request, 'accounts/login_request.html', {'form': form})

def verify_code(request):
    """Шаг 2: пользователь вводит e-mail и код, мы логиним его"""
    initial = {}
    if 'email' in request.GET:
        initial['email'] = request.GET['email']
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(username=email)
                if user.otp.is_valid(code):
                    login(request, user)
                    messages.success(request, 'Вы вошли в систему.')
                    user.otp.delete()
                    return redirect('board:post_list')
                messages.error(request, 'Неверный или просроченный код.')
            except (User.DoesNotExist, OneTimeCode.DoesNotExist):
                messages.error(request, 'Сначала запросите код.')
    else:
        form = VerifyForm(initial=initial)
    return render(request, 'accounts/verify.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('board:post_list')

