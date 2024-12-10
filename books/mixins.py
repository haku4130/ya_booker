from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user == self.get_object().added_by

    def handle_no_permission(self):
        return redirect(f'{self.login_url}?next={self.request.path}')


class StaffRequiredMixin:
    """
    Миксин для проверки, является ли пользователь сотрудником (is_staff).
    Если пользователь не является сотрудником, вызывает исключение PermissionDenied.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied(
                'У вас нет прав для доступа к этой странице.'
            )
        return super().dispatch(request, *args, **kwargs)
