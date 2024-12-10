from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler403, handler500, handler400

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

handler404 = 'books.views.custom_404'
handler403 = 'books.views.custom_403'
handler500 = 'books.views.custom_500'
handler400 = 'books.views.custom_400'
