"""
URL configuration for hitchhound project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

from issues import views as issues_views
from users import views as users_views
from projects import views as project_views
from notifications import views as notification_views
from reporting import views as reporting_views
from hitchhound import views as hitchhound_views

# Custom 404 error handler
handler404 = hitchhound_views.custom_404

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # User app routes
    path('accounts/login/', users_views.user_login, name='login'),
    path('signup/', users_views.user_signup, name='signup'),
    path('password_reset/done/', users_views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', users_views.password_reset_done, name='password_reset_confirm'),
    path('reset/done/', users_views.password_reset_complete, name='password_reset_complete'),
    path('profile/', users_views.user_profile, name='profile'),
    path('change_password/', users_views.change_password, name='change_password'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Issue app routes
    path('', issues_views.list_issues, name='home'),
    path('issues/', issues_views.list_issues, name='issues'),
    path('create_issue/', issues_views.create_issue, name='create_issue'),
    path('issues/<int:id>/', issues_views.issue_detail, name='issue_detail'),
    path('issues/<int:id>/edit/', issues_views.edit_issue, name='edit_issue'),
    path('issues/<int:id>/delete/', issues_views.delete_issue, name='delete_issue'),
    path('issues/<int:issue_id>/add_comment/', issues_views.add_comment, name='add_comment'),

    # Project app routes
    path('projects/', project_views.list_projects, name='projects'),
    path('projects/<int:project_id>/issues/', project_views.view_all_issues, name='view_all_issues'),
    path('create_project/', project_views.create_project, name='create_project'),
    path('edit_project/<int:id>/', project_views.edit_project, name='edit_project'),
    path('projects/<int:id>/delete/', project_views.delete_project, name='delete_project'),

    # Notification app routes
    path('notifications/', notification_views.list_notifications, name='notifications'),
    path('change_history/<int:issue_id>/', notification_views.change_history, name='issue_change_history'),

    # Reporting app routes
    path('reports/issue_listing_by_status/', reporting_views.issue_listing_by_status, name='issue_listing_by_status'),
    path('reports/issue_status_summary/', reporting_views.issue_status_summary, name='issue_status_summary'),
    path('reports/issue_severity_summary/', reporting_views.issue_severity_summary, name='issue_severity_summary'),
    path('reports/issue_listing_by_assignee/', reporting_views.issue_listing_by_assignee, name='issue_listing_by_assignee'),
]
