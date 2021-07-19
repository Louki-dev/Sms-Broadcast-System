from django.shortcuts import render, redirect
from django.contrib import messages
from Sms.forms import SignUpForm, EditprofileForm
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


def register_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/user/admin-login/")
        messages.error(request, "Username or password is already exists. Please try again.")
    form = SignUpForm()
    return render (request=request, template_name="registration/register.html", context={"form":form})


def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/user/admin/dashboard/")
        else:
            messages.error(request,"You have entered your password or username incorrectly.")
    return render(request=request, template_name="registration/login.html")


def logout_request(request):
    logout(request)
    return redirect("/user/admin-login/")


class user_profile(generic.UpdateView, SuccessMessageMixin):
    form_class = EditprofileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('admin')
    success_message = "Your profile has been successfully changed!"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        success_message = "Invalid information. Please try again."
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class password_change(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('admin')
    success_message = "Your password has been successfully changed!"

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        success_message = "Invalid information. Please try again."
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

