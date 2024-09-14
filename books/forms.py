from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import ReadingMark, Book, Chapter


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Название"


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        exclude = ('book',)

    def __init__(self, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Название"


class RegisterForm(UserCreationForm):
    """Form to Create new User"""

    usable_password = None

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            'email': forms.EmailInput(
                attrs={'placeholder': 'Почта для восстановления пароля'}
            ),
        }
