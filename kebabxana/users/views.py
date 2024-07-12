from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy

from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from cart.models import Cart

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def form_valid(self, form):
       
        remember_me = form.cleaned_data['remember_me'] 
        if not remember_me:
            self.request.session.set_expiry(0)  
            self.request.session.modified = True
        return super(LoginUser, self).form_valid(form)
    
    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()

                Cart.objects.filter(session_key=session_key).update(user=user)

                return HttpResponseRedirect(self.get_success_url())


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileUserForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:password_change_done')