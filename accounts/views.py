import re
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import FormView, View, TemplateView, CreateView, ListView, UpdateView, DeleteView

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, Address 
from .forms import UserLoginForm, CustomUserSignInForm, AddressCreationForm
from basket.views import basket_merge_after_login
from transaction.models import Transactions, Wallet

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^0[1-9][0-9]{9}$'

class LoginUser(FormView):
    form_class = UserLoginForm
    success_url = "/"
    template_name = "accounts/login.html"
    
    def post(self, request, *args, **kwargs):
        
        form = UserLoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            username = form.cleaned_data["email_phone"]
            if re.match(EMAIL_REGEX, username):
                user = authenticate(request, email=username, password=password)
            elif re.match(PHONE_REGEX, username):
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

class CreateUser(FormView):
    template_name = "accounts/signup.html"
    success_url = "/"
    form_class = CustomUserSignInForm
    
    def post(self, request, *args, **kwargs):
        form = CustomUserSignInForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            password2 = form.cleaned_data["password2"]
            phone_number = form.cleaned_data["phone_number"]
            lastname = form.cleaned_data["lastname"]
            firstname = form.cleaned_data["firstname"]
            email = form.cleaned_data["email"]
            if password2 != password:
                form.add_error("password", "passwords dont match")
            elif not re.match(EMAIL_REGEX, email):
                form.add_error("email", "email is wrong")
            elif not re.match(PHONE_REGEX, phone_number):
                form.add_error("phone_number", "phone number is wrong")
            if len(form.errors) > 0:
                return render(request, self.template_name, {"form":form})
            user = User.objects.create(email=email, username=email, phone_number=phone_number, firstname=firstname, lastname=lastname)
            user.set_password(password)
            user.save()
            login(self.request, user)
            return redirect(request.POST.get("next", "/"))
        return render(request, self.template_name, {"form":form})

class LogoutUser(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        response = HttpResponseRedirect("/")
        response.set_cookie('basket_id', '', max_age=0)
        return response
    
class Profile(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = User.objects.prefetch_related("addresses", "bookmarks", "basket").get(pk=self.request.user.pk) 
        ctx["user"] = user    
        ctx["address"] = user.addresses.all()
        ctx["bookmarks"] = user.bookmarks.all()
        ctx["last_products"] = user.basket.filter(is_paid=True) # last products user bought
        ctx["score"] = Transactions.calc_user_score(user.email)
        Wallet.update_wallet(user)
        w, _ = Wallet.objects.get_or_create(user=user)
        ctx["wallet"] = w
        return ctx

class CreateAddress(CreateView):
    form_class = AddressCreationForm
    context_object_name = "form"
    template_name = "accounts/address.html"
    success_url = "/accounts/profile"
    model = Address
    
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        addr = form.save(commit=False)
        addr.user = self.request.user
        addr.save()
        return HttpResponseRedirect(self.success_url)
    

class ListAddress(ListView):
    template_name = "accounts/address_list.html"
    context_object_name = "addresses"
    
    def get_queryset(self):
        queryset = Address.objects.filter(user=self.request.user)
        return queryset
    
class UpdateAddress(UpdateView):
    form_class = AddressCreationForm
    template_name = "accounts/address_update.html"
    context_object_name = "addresses"
    pk_url_kwarg = "id"
    success_url = "/accounts/profile"
    
    
    def get_queryset(self):
        id = self.kwargs["id"]
        queryset = Address.objects.filter(pk=id) 
        return queryset
    

class DeleteAddress(DeleteView):
    pk_url_kwarg = "id"
    success_url = "/accounts/profile"
    
    def get_queryset(self):
        id = self.kwargs["id"]
        queryset = Address.objects.filter(pk=id) 
        return queryset
    
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return HttpResponseRedirect(self.success_url)