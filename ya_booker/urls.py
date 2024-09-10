from django.contrib import admin
from django.urls import path, include

from books.views import UserRegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'accounts/registration/',
        UserRegistrationView.as_view(),
        name='registration',
    ),
    path('', include('books.urls')),
]
