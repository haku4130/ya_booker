from django import forms
from .models import ReadingMark, Book, Chapter


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

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
