from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import SignUpForm
from .models import BaseUser
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
            if password != password2:
                raise ValueError("Hasła nie są identyczne!")

            new_user = BaseUser.objects.create_user(email=email, password=password, first_name=first_name, birthday=birthday, last_name=last_name, is_active=False)
            new_user.save()
            return redirect('user-created-success')

    form = SignUpForm()
    return render(request, "signup_form.html", {'form': form})


class UserCreatedView(TemplateView):
    template_name = "user_created.html"


# class SignUpView(FormView):
#     template_name = 'signup_form.html'
#     form_class = SignUpForm
#     success_url = '/'
#
#     def form_valid(self, form):
#         breakpoint()
#         if form.password != form.password2:
#             raise ValueError("Hasła nie są identyczne!")
#         return super().form_valid(form)
