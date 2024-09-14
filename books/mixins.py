from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user == self.get_object().added_by

    def handle_no_permission(self):
        return redirect(f"{self.login_url}?next={self.request.path}")
