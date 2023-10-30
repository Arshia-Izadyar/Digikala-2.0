import re
from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import FormView, View

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .forms import UserLoginForm
from basket.views import basket_merge_after_login



class LoginUser(FormView):
    form_class = UserLoginForm
    success_url = "/"
    template_name = "accounts/login.html"
    
    def post(self, request, *args, **kwargs):
        email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone = r'^0[1-9][0-9]{9}$'
        form = UserLoginForm(request.POST)
        if form.is_valid():
            print("form valide")
            password = form.cleaned_data["password"]
            username = form.cleaned_data["email_phone"]
            if re.match(email, username):
                user = authenticate(request, email=username, password=password)
            elif re.match(phone, username):
                user = User.objects.get(phone_number=username)
                if not user.check_password(password):
                    form.add_error('password', 'Incorrect password for this phone number')
                    return render(request, self.template_name, {"form":form})
            if user is not None:
                login(self.request, user)
                response = HttpResponseRedirect(request.GET.get("next", "/"))
                basket = basket_merge_after_login(user, self.request)
                if basket is not None:
                    response.set_cookie("basket_id", basket.pk)
                return response 
            else:
                return render(request, self.template_name, {"form":form})
        return render(request, self.template_name, {"form":self.form_class})
    
class LogoutUser(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect("/")