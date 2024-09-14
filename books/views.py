from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
    FormView,
)
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseNotAllowed,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, authenticate


from .models import Book, ReadingMark, Chapter
from .forms import BookForm, ChapterForm, RegisterForm
from .tasks import create_reading_mark
from .mixins import AuthorRequiredMixin


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookForm()
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChapterForm()
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class BookUpdateView(AuthorRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_update_form.html'

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_content'] = 'Сохранить'
        return context


class BookDeleteView(AuthorRequiredMixin, DeleteView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('book_list')
    template_name = 'book_update_form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_content'] = 'Удалить'
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


class UserRegistrationView(FormView):
    template_name = 'registration/registration_form.html'
    form_class = RegisterForm
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class ProfileListView(ListView):
    model = Book
    template_name = 'profile.html'

    def get_user_profile(self):
        return get_object_or_404(get_user_model(), username=self.kwargs['username'])

    def get_queryset(self):
        user_profile = self.get_user_profile()
        return user_profile.books.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user_profile()
        return context
