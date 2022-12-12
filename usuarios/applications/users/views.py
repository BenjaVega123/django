from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import (CreateView, View)
from django.views.generic.edit import FormView
from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm, VerificationForm
from .models import User
from .functions import code_generator
# Create your views here.


class UserRegisterCreateView(FormView):
    template_name = "user/register.html"
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        #
        code = code_generator()
        #
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            names = form.cleaned_data['names'],
            lastname =  form.cleaned_data['lastname'],
            gender = form.cleaned_data['gender'],
            cod_reg = code,
        )
        #Send code to user
        subject = 'Confirmation code for django project'
        message = 'Verification code:' + code
        email_from = 'b.vegacceres@gmail.com'
        #
        send_mail(subject, message, email_from, [form.cleaned_data['email'],])
        # Redirect to validation page
        
        return HttpResponseRedirect(
            reverse(
                'users_app:verification_user',
                kwargs={'pk': usuario.id}
            )
        )

class LoginUser(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("home_app:home_page")

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'users_app:login_user'
            )
        )

class UpdatePassword(LoginRequiredMixin, FormView):
    template_name = 'user/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy("users_app:login_user")
    login_url= reverse_lazy("users_app:login_user")

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password=form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
        logout(self.request)
        return super(UpdatePassword, self).form_valid(form)

class CodeVer(FormView):
    template_name = 'user/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy("users_app:login_user")

    def get_form_kwargs(self):
        kwargs = super(CodeVer, self).get_form_kwargs()
        kwargs.update({
            'pk': self.kwargs['pk']
        })
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id = self.kwargs['pk']
        ).update(
            is_active = True
        )
        return super(CodeVer, self).form_valid(form)