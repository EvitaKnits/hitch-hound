from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
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
from django.db import models
from django.db.models.functions import Lower
from django.db.models import Q
from hitchhound.utils import paginate, get_new_notifications
from users.forms import UserProfileForm
from issues.models import Issue
from .forms import CustomUserCreationForm


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
                    # Determine protocol based on whether request is secure
                    protocol = 'https' if request.is_secure() else 'http'

                    # Render the email message with the calculated protocol
                    message = render_to_string(
                        'registration/password_reset_email.html',
                        {
                            'user': user,
                            'domain': current_site.domain,
                            'protocol': protocol,
                            'uid': uid,
                            'token': token,
                        }
                    )
                    try:
                        # Attempt to send the password reset email
                        send_mail(
                            mail_subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            [user.email]
                        )

                        # Notify the user of the success
                        messages.success(request, 'Password reset email sent.')

                        # Redirect to the password reset done page
                        return redirect('password_reset_done')

                    except Exception as e:
                        # Notify the user of the error
                        messages.error(request, f'Error sending email: {e}')

            else:
                messages.error(request, 'No user associated with this email.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = PasswordResetForm()

    return render(
        request, 'registration/password_reset_form.html', {'form': form}
    )


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

    if sort_by == 'title':
        issues = Issue.objects.filter(
            models.Q(reporter=user) |
            models.Q(developer=user) |
            models.Q(quality_assurance=user) |
            models.Q(product_manager=user)
        ).distinct().annotate(
            lower_title=Lower('title')
        ).order_by(
            f'{"" if order == "asc" else "-"}lower_title'
        )
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

    # Check if there's an alert type in the session and add it to the context
    alert_type = request.session.pop('Alert Type', None)

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
        'alert_type': alert_type,
    }
    return render(request, 'profile.html', context)


@login_required
def change_password(request):
    """ Handle password change functionality """
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(
            user=request.user, data=request.POST
        )
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            request.session['Alert Type'] = 'Password Changed'
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
