# accounts/views.py

from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from allauth.account.views import PasswordChangeView


# Without this custom class, PasswordChangeView redirects to itself
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse_lazy('password_change_success')
    

class PasswordChangeSuccessView(generic.TemplateView):
    template_name = "account/password_change_success.html"


class SignUpPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"