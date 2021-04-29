from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, UpdateUserDataForm
from .models import BaseUser
from .tokens import account_invitation_token


# Create your views here.


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            birthday = form.cleaned_data.get('birthday')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            is_teacher = form.cleaned_data.get('is_teacher', False)
            if password != password2:
                raise ValueError("Hasła nie są identyczne!")

            new_user = BaseUser.objects.create_user(email=email,
                                                    password=password,
                                                    first_name=first_name,
                                                    birthday=birthday,
                                                    last_name=last_name,
                                                    is_active=False,
                                                    is_teacher=is_teacher)
            new_user.save()
            token = account_invitation_token.make_token(user=new_user)
            user_uid = urlsafe_base64_encode(force_bytes(new_user.pk))
            activate_url = f"{request.scheme}://{request.get_host()}/user/{user_uid}/activate/{token}"
            mail_sent = send_mail(
                "Tutorex - aktywuj swoje konto",
                f"Oto twój link aktywacyjny, kliknij w niego aby aktywować swoje konto w aplikacji Tutorex: {activate_url}",
                settings.EMAIL_HOST_USER,
                [email], fail_silently=False
            )
            if mail_sent == 0:
                raise ValueError("Nie udało się wysłać maila aktywacyjnego!")

            return redirect('user-created-success')

    form = SignUpForm()
    return render(request, "signup_form.html", {'form': form})


class UserCreatedView(TemplateView):
    template_name = "user_created.html"



class ActivateUserView(View):

    def get(self, request, user_uid, token, *args, **kwargs):
        user = None
        try:
            user_id = force_text(urlsafe_base64_decode(user_uid))
            user = BaseUser.objects.get(pk=user_id)
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user is not None and not user.is_active and account_invitation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('user-activated-view', user_id=user.id)
        else:
            raise ValueError(
                "Nie udało się aktywować konta, być może link użyty do aktywacji jest nieprawidłowy, albo został już wykorzystany!"
            )


class UserActivatedView(View):

    def get(self, request, user_id, *args, **kwargs):
        user = BaseUser.objects.get(pk=user_id)
        context = {'user': user}

        return render(request, "user_activated.html", context=context)


def index_view(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    return render(request, "index.html", {'is_authenticated': request.user.is_authenticated, 'user': user})


def user_login(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if request.GET.get("next", None):
                return redirect(request.GET["next"])
            return redirect('user-success')
        else:
            context["error"] = "Email lub haslo są nieprawidlowe"
            return render(request, "login.html", context=context)
    else:
        return render(request, "login.html", context=context)


@login_required(login_url="/login/")
def success(request):
    context = {}
    context["user"] = request.user
    return render(request, "success.html", context=context)


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('user-login')


class EditUserProfileView(LoginRequiredMixin, View):

    def get(self, request, user_id, *args, **kwargs):
        user = None
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id:
                return HttpResponseForbidden("You cannot edit data of users except your own!")

        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
            raise ValueError("Ojojojoj! Coś poszło nie tak :(")
        form = UpdateUserDataForm()
        return render(request, "profile_form.html", {form: 'form', 'user': user})

    def post(self, request, user_id, *args, **kwargs):
        user = None
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id:
                return HttpResponseForbidden("You cannot edit data of users except your own!")

        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
            raise ValueError("Ojojojoj! Coś poszło nie tak :(")
        form = UpdateUserDataForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
            user.save()
        return redirect('index')
