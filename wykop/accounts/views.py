from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views.generic import FormView

from wykop.accounts.forms import RegisterForm


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse('posts:list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('posts:list')
