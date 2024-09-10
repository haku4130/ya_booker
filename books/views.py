from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Book, ReadingMark, Chapter, RegisterForm
from .forms import BookForm, ChapterForm
from .tasks import create_reading_mark


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookForm()
        return context


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('book_list')


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk': self.kwargs['pk']})


class BookDeleteView(DeleteView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('book_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChapterForm()
        return context


class ChapterCreateView(CreateView):
    model = Chapter
    form_class = ChapterForm

    def form_valid(self, form):
        form.instance.book = get_object_or_404(Book, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk': self.kwargs['pk']})


@login_required
def create_reading_mark_view(request, book_pk, chapter_pk):
    if request.method == 'POST':
        chapter = get_object_or_404(Chapter, pk=chapter_pk)
        create_reading_mark.delay(chapter.id, request.user.id)
        return redirect(reverse('book_detail', kwargs={'pk': book_pk}))

    return HttpResponseBadRequest("Invalid request method")


class UserRegistrationView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = RegisterForm
    success_url = reverse_lazy('book_list')


class ProfileListView(ListView):
    model = Book
    template_name = 'profile.html'

    def get_user_profile(self):
        return get_object_or_404(
            get_user_model(), username=self.kwargs['username']
        )

    def get_queryset(self):
        user_profile = self.get_user_profile()
        return user_profile.books.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user_profile()
        return context
