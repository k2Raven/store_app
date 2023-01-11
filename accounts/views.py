from django.contrib.auth import get_user_model,login,  update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import MultipleObjectMixin

from accounts.forms import MyUserCreationForm



class RegisterView(CreateView):
    model = get_user_model()
    form_class = MyUserCreationForm
    template_name = 'user_create.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url

        next_url = self.request.POST.get('next')
        if next_url:
            return next_url

        return reverse('webapp:index')




