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
from issues import views as issues_views
from users import views as users_views
from projects import views as project_views
from notifications import views as notification_views
from reporting import views as reporting_views

urlpatterns = [
    path('', issues_views.list_issues, name='home'),
    path('issues', issues_views.list_issues, name='issues'),
    path('login/', users_views.user_login, name='login'),
    path('logout/', users_views.user_logout_confirm, name='logoutconfirm'),
    path('signup/', users_views.user_signup, name='signup'),
    path('password_reset/', users_views.password_reset, name='reset'),
    path('password_reset/done/', users_views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', users_views.password_reset_done, name='password_reset_confirm'),
    path('reset/done/', users_views.password_reset_complete, name='password_reset_complete'),
    path('profile/', users_views.user_profile, name='profile'),
    path('create_issue/', issues_views.create_issue, name='create_issue'),
    path('issues/<int:issue_id>/', issues_views.issue_detail, name='issue_detail'),
    path('issues/<int:issue_id>/edit/', issues_views.edit_issue, name='edit_issue'),
    path('issues/<int:pk>/delete/', issues_views.delete_issue, name='delete_issue'),
    path('projects/', project_views.list_projects, name='projects'),
    path('projects/<int:pk>/issues/', project_views.view_all_issues, name='view_all_issues'),
    path('create_project/', project_views.create_project, name='create_project'),
    path('edit_project/<int:pk>/', project_views.edit_project, name='edit_project'),
    path('not_found/', notification_views.not_found, name='not_found' ),
    path('notifications/', notification_views.list_notifications, name='notifications'),
    path('change_history/', notification_views.change_history, name='change_history'),
    path('reports/', reporting_views.list_reports, name='reports'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]