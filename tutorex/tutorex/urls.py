"""tutorex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from lessons import views as lesson_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.index_view, name='index'),
    path('signup-choice/', user_views.SignupTypeChoiceView.as_view(), name='signup-choice-view'),
    path('signup/', user_views.signup, name='signup-view'),
    path('signup/parent', user_views.signup_parent, name='signup-view-parent'),
    path('signup/teacher', user_views.signup, name='signup-view-teacher'),
    path('signup/done', user_views.UserCreatedView.as_view(), name='user-created-success'),
    path('user/<user_uid>/activate/<token>', user_views.ActivateUserView.as_view(), name='user-activate'),
    path('user/<user_id>/activated', user_views.UserActivatedView.as_view(), name="user-activated-view"),
    path('login/', user_views.index_view, name='user-login'),
    path('success/', user_views.success, name='user-success'),
    path('logout/', user_views.user_logout, name='user-logout'),
    path('user/<user_id>/edit', user_views.EditUserProfileView.as_view(), name='user-edit-data'),
    path('user/<user_id>/password/edit', user_views.ChangePasswordView.as_view(), name='user-change-password'),
    path('request-reset-link/', user_views.RequestResetPasswordEmail.as_view(), name='request-password'),
    path('user/<user_uid>/reset-password/<token>', user_views.CompletePasswordReset.as_view(), name='reset-user-password'),
    path('link-send/', user_views.link_send, name='link-send')
]
