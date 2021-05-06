from django.conf import settings
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .forms import SignUpForm, SignUpParentForm, UpdateUserDataForm
from .models import BaseUser
from .tokens import account_invitation_token


# Create your views here.

@csrf_protect
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
    template_to_render = "signup_form.html"
    if request.get_full_path() == '/signup/teacher':
        template_to_render = "signup_form_teacher.html"
    return render(request, template_to_render, {'form': form})


@csrf_protect
def signup_parent(request):
    if request.method == "POST":
        form = SignUpParentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            birthday = form.cleaned_data.get('birthday')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')
            parent_pass = form.cleaned_data.get('parent_password')
            parent_pass2 = form.cleaned_data.get('parent_password2')
            if password != password2:
                raise ValueError("Hasła nie są identyczne!")
            if parent_pass != parent_pass2:
                raise ValueError("Hasła dla rodzica nie są identyczne!")
            new_user = BaseUser.objects.create_user(email=email,
                                                    password=password,
                                                    parent_password=parent_pass,
                                                    first_name=first_name,
                                                    birthday=birthday,
                                                    last_name=last_name,
                                                    is_active=False)
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

    form = SignUpParentForm()
    return render(request, "signup_form_parent.html", {'form': form})


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
            return render(request, "index.html", context=context)
    else:
        return render(request, "index.html", context=context)


@login_required(login_url="/login/")
def success(request):
    context = {}
    context["user"] = request.user
    return render(request, "success.html", context=context)


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')


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


def link_send(request):
    return render(request, "link_send.html")


class RequestResetPasswordEmail(View):
    def get(self, request):
        return render(request, "reset_password.html")

    def post(self, request):
        context = {}
        email = request.POST['email']
        # if not validate_email(email):
        #    context['error'] = "Podaj legitnego maila"
        #    return render(request, "reset_password.html", context)

        try:
            user = BaseUser.objects.filter(email=email)
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None

        if user.exists():
            user_uid = urlsafe_base64_encode(force_bytes(user[0].pk))
            token = PasswordResetTokenGenerator().make_token(user[0])
            reset_passwd_url = f"{request.scheme}://{request.get_host()}/user/{user_uid}/reset-password/{token}"
            mail_sent = send_mail(
                "Tutorex - zresetuj swoje hasło",
                f"Kliknij w poniższy link aby zresetować swoje hasło: \n {reset_passwd_url}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            if mail_sent == 0:
                raise ValueError("Nie udało się wysłać maila resetującego hasło :(")

            return redirect('link-send')
        else:
            context['error'] = "Bro ... próbujesz się komuś na konto włamać? o.O"
            return render(request, "reset_password.html", context)


class CompletePasswordReset(View):
    def get(self, request, user_uid, token):
        context = {
            "user_uid": user_uid,
            "token": token
        }
        return render(request, "set_new_password.html", context=context)

    def post(self, request, user_uid, token):
        context = {
            "user_uid": user_uid,
            "token": token
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            context['error'] = "Hasła nie są identyczne!"
            return render(request, "set_new_password.html", context=context)

        # if len(password) < 6:
        #    context['error'] = "Hasła za krótkie!"
        #    return render(request, "set_new_password.html", context=context)

        try:
            user_id = force_text(urlsafe_base64_decode(user_uid))
            user = BaseUser.objects.get(pk=user_id)
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
            context['error'] = "Coś poszło nie tak, spróbuj ponownie"
            return render(request, "set_new_password.html", context=context)

        if user is not None:
            user.set_password(password)
            user.save()
            context['success'] = "Hasło zmienione pomyślnie"
            return redirect('user-login')
