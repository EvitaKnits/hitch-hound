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
from django.urls import path
from issues import views as issues_views
from users import views as users_views
from projects import views as project_views

urlpatterns = [
    path('login/', users_views.user_login, name='login'),
    path('signup/', users_views.user_signup, name='signup'),
    path('reset/', users_views.password_reset, name='reset'),
    path('profile/', users_views.user_profile, name='profile'),
    path('issues/', issues_views.list_issues, name='issues'),
    path('newissue/', issues_views.create_issue, name='newissue'),
    path('editissue/', issues_views.edit_issue, name='editissue'),
    path('projects/', project_views.list_projects, name='projects'),
    path('newproject/', project_views.new_project, name='newproject'),
    path('editproject/', project_views.edit_project, name='editproject'),
    path('admin/', admin.site.urls),
]
