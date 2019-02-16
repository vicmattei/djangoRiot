from django.views import generic
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm

from . import models


class UserCreateView(generic.CreateView):
    model = models.User
    form_class = UserCreationForm

    def get_success_url(self, *args, **kwargs):
        return reverse('redirect')
