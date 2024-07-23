from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from issues.models import Issue, UserIssue
from django.db import models
from hitchhound.utils import paginate, get_new_notifications
from users.forms import UserProfileForm
from django.db.models.functions import Lower
from django.db.models import F, Q
from notifications.models import Change
from django.utils import timezone

def user_login(request):
    """ View to handle user login functionality """
    context = {'show_register_navbar': True}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            context['error_message'] = 'Invalid username or password.'

    return render(request, 'login.html', context)

def user_signup(request):
    """ View to handle user signup functionality """
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
    """ View to handle password reset functionality """
    if request.method == 'POST':
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
    """ Render the password reset done view """
    return render(request, 'registration/password_reset_done.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """ Custom view for confirming password reset """
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

def password_reset_complete(request):
    """ Render the password reset complete view """
    return render(request, 'registration/password_reset_complete.html')

@login_required
def user_profile(request):
    """ Handle user profile view, form submission, and issue sorting """
    user = request.user
    sort_by = request.GET.get('sort_by', 'id')
    order = request.GET.get('order', 'asc')
    toggle_order = 'desc' if order == 'asc' else 'asc'

    # Determine the sorting field and annotation
    if sort_by == 'title':
        issues = Issue.objects.filter(
            models.Q(reporter=user) |
            models.Q(developer=user) |
            models.Q(quality_assurance=user) |
            models.Q(product_manager=user)
        ).distinct().annotate(lower_title=Lower('title')).order_by(f'{'' if order == 'asc' else '-'}lower_title')
    else:
        issues = Issue.objects.filter(
            models.Q(reporter=user) |
            models.Q(developer=user) |
            models.Q(quality_assurance=user) |
            models.Q(product_manager=user)
        ).distinct().order_by(f'{'' if order == 'asc' else '-'}{sort_by}')

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        if 'save_profile' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user)

    # Use the paginate utility function to handle pagination
    page_obj = paginate(request, issues)

    # Calculate new notifications for the current user
    new_notifications = get_new_notifications(request.user)

    context = {
        'form': profile_form,
        'username': user.username,
        'page_obj': page_obj,
        'sort_by': sort_by,
        'order': order,
        'toggle_order': toggle_order,
        'new_notifications': new_notifications,
        'active_page': 'profile',
        'show_navbar': True,
    }
    return render(request, 'profile.html', context)

@login_required
def change_password(request):
    """ Handle password change functionality """
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        password_change_form = PasswordChangeForm(user=request.user)
    
    # Calculate new notifications for current user
    new_notifications = get_new_notifications(request.user)

    context = {
        'password_change_form': password_change_form,
        'new_notifications': new_notifications,
        'active_page': 'profile',
        'show_navbar': True,
    }

    return render(request, 'change_password.html', context)
