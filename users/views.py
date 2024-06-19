from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.views import PasswordResetConfirmView

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'login.html')

def user_logout_confirm(request):
    return render(request, 'logoutconfirm.html', {'active_page': 'logout'})

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['registration_success'] = True
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = form.get_users(email)
            if users:
                for user in users:
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    current_site = get_current_site(request)
                    mail_subject = 'Password reset'
                    message = render_to_string('registration/password_reset_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'protocol': 'https' if request.is_secure() else 'http',
                        'uid': uid,
                        'token': token,
                    })
                    try:
                        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
                        messages.success(request, 'Password reset email has been sent.')
                        return redirect('password_reset_done')
                    except Exception as e:
                        messages.error(request, f'Error sending email: {e}')
            else:
                messages.error(request, 'No user is associated with this email address.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset_form.html', {'form': form})


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')

def user_profile(request):
    return render(request, 'profile.html', {'active_page': 'profile'})