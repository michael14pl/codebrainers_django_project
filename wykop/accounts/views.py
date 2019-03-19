from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView, UpdateView

from wykop.accounts.forms import RegisterForm
from wykop.accounts.models import User


class LogoutRequiredMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
        return super().dispatch(request, *args, **kwargs)


class RegisterView(LogoutRequiredMixin, FormView):
    form_class = RegisterForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse('posts:list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserLoginView(LogoutRequiredMixin, LoginView):
    template_name = 'login.html'


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'profile'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    fields = ('first_name', 'last_name', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'accounts:profile',
            args=(self.request.user.pk, )
        )
