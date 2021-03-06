from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from django.forms import model_to_dict
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, View
from django.views.generic.edit import DeleteView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator, default_token_generator
from django.template import loader
from notifications.signals import notify
from notifications.utils import id2slug
import datetime
from dateutil.relativedelta import relativedelta
import locale
import pytz
import json
from .forms import SignUpForm, SignUpParentForm, UpdateUserDataForm, ChangePasswordForm
from .models import BaseUser
from .tokens import account_invitation_token


def get_16_ya():
    user_16_years = datetime.date.today() - relativedelta(years=16)
    user_16_years = user_16_years.strftime("%Y-%m-%d")
    return user_16_years


def get_today_date():
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    return current_date


@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

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
                raise ValueError("Has??a nie s?? identyczne!")

            new_user = BaseUser.objects.create_user(email=email,
                                                    password=password,
                                                    first_name=first_name,
                                                    birthday=birthday,
                                                    last_name=last_name,
                                                    is_active=False,
                                                    is_teacher=is_teacher)

            # res = validate_password(password, new_user)
            new_user.save()
            token = account_invitation_token.make_token(user=new_user)
            user_uid = urlsafe_base64_encode(force_bytes(new_user.pk))
            activate_url = f"{request.scheme}://{request.get_host()}/user/{user_uid}/activate/{token}"
            html_message = loader.render_to_string('activate_email_temp.html',
                                                   {'user_name': new_user.first_name, 'activate_link': activate_url})

            mail_sent = send_mail(
                "Tutorex - aktywuj swoje konto",
                '',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=html_message
            )
            if mail_sent == 0:
                raise ValueError("Nie uda??o si?? wys??a?? maila aktywacyjnego!")

            return redirect('user-created-success')

    form = SignUpForm()
    user_16_years = get_16_ya()
    template_to_render = "signup_form.html"
    if request.get_full_path() == '/signup/teacher':
        template_to_render = "signup_form_teacher.html"
    return render(request, template_to_render, {'form': form, 'user_16_years': user_16_years})


@csrf_protect
def signup_parent(request):
    if request.user.is_authenticated:
        return redirect("home")
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
                raise ValueError("Has??a nie s?? identyczne!")
            if parent_pass != parent_pass2:
                raise ValueError("Has??a dla rodzica nie s?? identyczne!")
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
            html_message = loader.render_to_string('activate_email_temp.html',
                                                   {'user_name': new_user.first_name, 'activate_link': activate_url})

            mail_sent = send_mail(
                "Tutorex - aktywuj swoje konto",
                '',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=html_message
            )
            if mail_sent == 0:
                raise ValueError("Nie uda??o si?? wys??a?? maila aktywacyjnego!")

            return redirect('user-created-success')

    user_16_years = get_16_ya()
    today = get_today_date()
    form = SignUpParentForm()
    return render(request, "signup_form_parent.html", {'form': form, 'user_16_years': user_16_years, 'today': today})


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
                "Nie uda??o si?? aktywowa?? konta, by?? mo??e link u??yty do aktywacji jest nieprawid??owy, albo zosta?? ju?? wykorzystany!"
            )


class UserActivatedView(View):

    def get(self, request, user_id, *args, **kwargs):
        user = BaseUser.objects.get(pk=user_id)
        context = {'user': user}

        return render(request, "user_activated.html", context=context)


class SignupTypeChoiceView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "register_type.html", context={})


@login_required(login_url="/login/")
def home_view(request):
    return render(request, "main.html", {'user': request.user})


def index_view(request):
    if request.user.is_authenticated:
        return redirect("home")
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
            context["error"] = "Email lub haslo s?? nieprawidlowe"
            return render(request, "index.html", context=context)
    else:
        return render(request, "index.html", context=context)


@login_required(login_url="/login/")
def success(request):
    # context = {}
    # context["user"] = request.user
    # return render(request, "success.html", context=context)
    return redirect("home")


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')


class EditUserProfileView(LoginRequiredMixin, View):

    def get(self, request, user_id, *args, **kwargs):
        user = None
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id or not request.user.id:
                raise PermissionDenied

        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
            raise ValueError("Ojojojoj! Co?? posz??o nie tak :(")

        age_constr = get_16_ya()
        today = get_today_date()
        return render(request, "account.html", {'user': user, 'user_18_years': age_constr, 'today': today})

    def post(self, request, user_id, *args, **kwargs):
        user = None
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id or not request.user.id:
                raise PermissionDenied

        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
            raise ValueError("Ojojojoj! Co?? posz??o nie tak :(")
        form = UpdateUserDataForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            birthday = form.cleaned_data.get('birthday')
            # email = form.cleaned_data.get('email')
            # phone_number = form.cleaned_data.get('phone_number')
            user.first_name = first_name
            user.last_name = last_name
            user.birthday = birthday
            # user.email = email
            # user.phone_number = phone_number
            user.save()
        return render(request, "account.html", {'user': user})


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id or not request.user.id:
                raise PermissionDenied
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user:
            return render(request, "change_password.html")

    def post(self, request, user_id):
        context = {}
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id or not request.user.id:
                raise PermissionDenied
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data.get('old_password')
                password = form.cleaned_data.get('password')
                password2 = form.cleaned_data.get('password2')
                if not (check_password(old_password, user.password) and password == password2):
                    raise ValueError("Stare has??o jest nieprawid??owe, albo podane nowe has??a r????ni?? si?? od siebie!")
                else:
                    user.set_password(password)
                    user.save()
                    context['success'] = "Has??o zmienione pomy??lnie"
                    return redirect('user-login')

        else:
            context['error'] = "Ojojoj! Co?? posz??o nie tak!"
            return render(request, "change_password.html", context)


class ChangeParentPasswordView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id or not request.user.id or request.user.parent_password is None:
                raise PermissionDenied
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user:
            return render(request, "change_parent_password.html")

    def post(self, request, user_id):
        context = {}
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id or not request.user.id or request.user.parent_password is None:
                raise PermissionDenied
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                old_password = form.cleaned_data.get('old_password')
                password = form.cleaned_data.get('password')
                password2 = form.cleaned_data.get('password2')
                print(old_password)
                print(user.parent_password)
                if not (user.parent_password == old_password and password == password2):
                    print('lol')
                    context['error'] = "Ojojoj! Co?? posz??o nie tak!"
                    return render(request, "change_parent_password.html", context)
                else:
                    print('lol2')
                    user.parent_password = password
                    user.save()
                    context['success'] = 'Has??o rodzica zmieniono pomy??lnie'
                    return redirect('home')
        else:
            context['error'] = "Ojojoj! Co?? posz??o nie tak!"
            return render(request, "change_parent_password.html", context)


class DeleteUser(LoginRequiredMixin, View):
    def get(self, request, user_id):
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id or not request.user.id:
                raise PermissionDenied
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user:
            return render(request, "delete_user.html")

    def post(self, request, user_id):
        context = {}
        try:
            user = BaseUser.objects.get(pk=user_id)
            if user.id != request.user.id or not request.user.id:
                raise PermissionDenied
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user:
            if request.method == "POST":
                password = request.POST.get('password')
                parent_password = request.POST.get('parent_password')
                if user.parent_password is not None:
                    if parent_password == '':
                        context['error'] = 'Musisz poda?? has??o rodzica!'
                        return render(request, 'delete_user.html', context=context)
                    if not (check_password(password, user.password)):
                        context['error'] = 'Podane has??o jest nieprawid??owe!'
                        return render(request, 'delete_user.html', context=context)
                    if parent_password != user.parent_password:
                        context['error'] = 'Podane has??o rodzica jest nieprawid??owe!'
                        return render(request, 'delete_user.html', context=context)
                    user.delete()
                    return redirect('user-login')
                else:
                    if not (check_password(password, user.password)):
                        context['error'] ="Has??o jest nieprawid??owe!"
                        return render(request, 'delete_user.html', context=context)
                    user.delete()
                    return redirect('user-login')
            else:
                context['error'] = "Co?? nie teges"
                return render(request, 'delete_user.html', context)
        else:
            return render(request, 'delete_user.html')


def link_send(request):
    return render(request, "link_send.html")


class RequestResetParentPasswordEmail(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "reset_parent_password.html")

    def post(self, request):
        context = {}
        email = request.POST['email']
        try:
            user = BaseUser.objects.filter(email=email)
            print(user)
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
        if user[0].parent_password is None:
            raise PermissionDenied
        if user:
            user_uid = urlsafe_base64_encode(force_bytes(user[0].pk))
            token = PasswordResetTokenGenerator().make_token(user[0])
            reset_passwd_url = f"{request.scheme}://{request.get_host()}/user/{user_uid}/reset-parent-password/{token}"
            html_message = loader.render_to_string('reset_parent_email_temp.html',
                                                   {'user_name': user[0].first_name, 'reset_link': reset_passwd_url})
            print("wysy??am maila")
            mail_sent = send_mail(
                "Tutorex - zresetuj swoje has??o rodzica",
                '',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=html_message
            )
            if mail_sent == 0:
                raise ValueError("Nie uda??o si?? wys??a?? maila resetuj??cego has??o :(")

            return redirect('link-send')
        else:
            context['error'] = "Bro ... rodzicowi has??o pr??bujesz zmieni??? o.O"
            return render(request, "reset_parent_password.html", context)


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

        if user:
            user_uid = urlsafe_base64_encode(force_bytes(user[0].pk))
            token = PasswordResetTokenGenerator().make_token(user[0])
            reset_passwd_url = f"{request.scheme}://{request.get_host()}/user/{user_uid}/reset-password/{token}"
            html_message = loader.render_to_string('reset_email_temp.html',
                                                   {'user_name': user[0].first_name, 'reset_link': reset_passwd_url})

            mail_sent = send_mail(
                "Tutorex - zresetuj swoje has??o",
                '',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=html_message
            )
            if mail_sent == 0:
                raise ValueError("Nie uda??o si?? wys??a?? maila resetuj??cego has??o :(")

            return redirect('link-send')
        else:
            context['error'] = "Bro ... pr??bujesz si?? komu?? na konto w??ama??? o.O"
            return render(request, "reset_password.html", context)


class CompleteParentPasswordReset(View):
    def get(self, request, user_uid, token):
        context = {
            "user_uid": user_uid,
            "token": token
        }
        return render(request, "set_new_parent_password.html", context=context)

    def post(self, request, user_uid, token):
        context = {
            "user_uid": user_uid,
            "token": token
        }
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            context['error'] = "Has??a nie s?? identyczne!"
            return render(request, "set_new_parent_password.html", context=context)

        try:
            user_id = force_text(urlsafe_base64_decode(user_uid))
            user = BaseUser.objects.get(pk=user_id)
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
            context['error'] = "Co?? posz??o nie tak, spr??buj ponownie"
            return render(request, "set_new_password.html", context=context)

        if user is not None:
            user.parent_password = password
            user.save()
            context['success'] = "Has??o rodzica zmienione pomy??lnie"
            return redirect('home')


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
            context['error'] = "Has??a nie s?? identyczne!"
            return render(request, "set_new_password.html", context=context)

        # if len(password) < 6:
        #    context['error'] = "Has??a za kr??tkie!"
        #    return render(request, "set_new_password.html", context=context)

        try:
            user_id = force_text(urlsafe_base64_decode(user_uid))
            user = BaseUser.objects.get(pk=user_id)
        except (ValueError, TypeError, OverflowError, BaseUser.DoesNotExist):
            user = None
            context['error'] = "Co?? posz??o nie tak, spr??buj ponownie"
            return render(request, "set_new_password.html", context=context)

        if user is not None:
            print('Dlaczegoooo')
            user.set_password(password)
            user.save()
            context['success'] = "Has??o zmienione pomy??lnie"
            return redirect('user-login')


class NotificationsView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        new_notifications = user.notifications.all()
        request_timestamp = datetime.datetime.now()
        request_timestamp = request_timestamp.replace(tzinfo=pytz.utc)
        for n in new_notifications:
            if abs(request_timestamp - n.timestamp).days > 7:
                n.unread = False
                n.save()

        new_notifications = [line for line in new_notifications if abs(request_timestamp - line.timestamp).days <= 7]
        return render(request, "notifications_view.html", {'all_count': len(new_notifications), "notifications": new_notifications})

class Contact(View):
    def get(self, request, *args, **kwargs):
        return render(request, "contact_us.html")


class Terms(View):
    def get(self, request, *args, **kwargs):
        return render(request, "terms.html")        


def get_user_notifications(request):
    user = request.user
    locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
    new_notifications = user.notifications.all()
    request_timestamp = datetime.datetime.now()
    request_timestamp = request_timestamp.replace(tzinfo=pytz.utc)
    for n in new_notifications:
        if abs(request_timestamp - n.timestamp).days > 7:
            n.unread = False
            n.save()
    new_notifications = [line for line in new_notifications if abs(request_timestamp - line.timestamp).days <= 7]
    all_list = []
    for notification in new_notifications:
        struct = model_to_dict(notification)
        struct['slug'] = id2slug(notification.id)
        struct['id'] = str(notification.id)
        struct['timestamp'] = str(notification.timestamp.strftime("%d %B %Y %H:%M %p"))
        if notification.actor:
            struct['actor'] = str(notification.actor)
        if notification.target:
            struct['target'] = str(notification.target)
        elif notification.recipient:
            struct['target'] = str(notification.recipient)
        if notification.action_object:
            struct['action_object'] = str(notification.action_object)
        if notification.data:
            struct['verb'] = notification.verb
        struct['unread'] = notification.unread
        struct['need_acceptance'] = notification.data.get('need_acceptance', False) if isinstance(notification.data, dict) else False

        all_list.append(struct)
    data = {
        'notifications': all_list[::-1],
        'all_count': len(new_notifications),
    }
    return JsonResponse(data)


def validate_pass(request):
    password = request.POST.get('password')
    try:
        res = validate_password(password)
    except Exception as e:
        data = {'pass_error': e.messages[0]}
        return JsonResponse(data)

    return JsonResponse({})


@csrf_exempt
def check_email_exists(request):
    email = request.POST.get('email')
    user = BaseUser.objects.filter(email=email)
    data = dict()
    if user:
        data['valid'] = False
        data['mail_error'] = 'U??ytkownik o podanym mailu ju?? istnieje!'
        return JsonResponse(data)

    data['valid'] = True
    return JsonResponse(data)


@login_required(login_url="/login/")
def check_if_password_matches(request):
    password = request.POST.get('password')
    if request.POST.get('parent'):
        data = {
            'matches': password == request.user.parent_password,
        }
    else:
        user = authenticate(request, username=request.user.email, password=password)
        data = {
            'matches': True if user else False,
        }
    return JsonResponse(data)


@login_required(login_url="/login/")
def parent_password_validate(request):
    user = request.user
    if not request.is_ajax():
        return HttpResponse(status=403)
    parent_pass = request.POST.get('parent_password')
    parent_pass2 = request.POST.get('parent_password2')
    if parent_pass != parent_pass2:
        return HttpResponse(status=403)
    if parent_pass != user.parent_password:
        return HttpResponse(status=403)

    return HttpResponse(status=200)


def handler_404(request, exception, template_name='404.html'):
    if request.user.is_authenticated:
        template_name = '404_auth.html'
    return render(request, template_name, status=404)


def handler_500(request, *args, **kwargs):
    template_name = '500_auth.html' if request.user.is_authenticated else '500.html'
    return render(request, template_name, status=500)


def handler_403(request, exception, template_name='403.html'):
    message = exception.args[0] if exception.args else None
    template_name = '403_auth.html' if request.user.is_authenticated else '403.html'
    return render(request, template_name, {'message': message}, status=403)
