from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Book, Chapter, Feedback


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Название'


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        exclude = ('book',)

    def __init__(self, *args, **kwargs):
        super(ChapterForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Название'


class RegisterForm(UserCreationForm):
    """Form to Create new User"""

    usable_password = None

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(
                attrs={'placeholder': 'Почта для восстановления пароля'}
            ),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Введите ваше сообщение...'}
            ),
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label='Поиск')
    search_in = forms.MultipleChoiceField(
        choices=[
            ('title', 'Название книги'),
            ('author', 'Имя автора'),
            ('chapter', 'Название главы'),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Искать в',
    )
