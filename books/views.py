from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
    FormView,
)
from django.http import (
    HttpResponseRedirect,
)

from .models import Book, Chapter, Feedback
from .forms import (
    BookForm,
    ChapterForm,
    RegisterForm,
    FeedbackForm,
    SearchForm,
)
from .tasks import (
    create_reading_mark,
    get_fully_read_books,
    get_partially_read_books,
    get_reading_users,
    get_completed_users,
)
from .mixins import AuthorRequiredMixin, StaffRequiredMixin


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data.get('query')
            search_in = form.cleaned_data.get('search_in')

            if query:
                q_objects = Q()

                if 'title' in search_in:
                    q_objects |= Q(title__icontains=query)

                if 'author' in search_in:
                    q_objects |= Q(added_by__username__icontains=query)

                if 'chapter' in search_in:
                    q_objects |= Q(chapters__title__icontains=query)

                queryset = queryset.filter(q_objects).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookForm()
        form = SearchForm(self.request.GET)
        context['search_form'] = form

        if form.is_valid():
            context['query'] = form.cleaned_data.get('query')
            context['search_in'] = form.cleaned_data.get('search_in')
        return context


# def get_queryset(self):
#         queryset = super().get_queryset()
#         search_query = self.request.GET.get('search', '')

#         if search_query:
#             queryset = queryset.filter(
#                 Q(title__icontains=search_query)
#                 | Q(chapters__title__icontains=search_query)
#                 | Q(added_by__username__icontains=search_query)
#             ).distinct()

#         return queryset


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context['chapters'] = [
                (chapter, chapter.read_marks.filter(user=user).exists())
                for chapter in self.get_object().chapters.all()
            ]
        else:
            # Если пользователь не аутентифицирован, просто передаем главы без отметок
            context['chapters'] = [
                (
                    chapter,
                    False,
                )  # False, т.к. анонимный пользователь не может иметь отметок
                for chapter in self.get_object().chapters.all()
            ]

        context['reading_users'] = get_reading_users(self.get_object())
        context['completed_users'] = get_completed_users(self.get_object())
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
    context_object_name = 'book'
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


class ChapterUpdateView(UpdateView):
    model = Chapter
    form_class = ChapterForm
    context_object_name = 'chapter'
    template_name = 'chapter_update_form.html'

    def get_object(self):
        return get_object_or_404(
            Chapter, pk=self.kwargs['chapter_pk'], book_id=self.kwargs['pk']
        )

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_content'] = 'Сохранить'
        return context


@login_required
def create_reading_mark_view(request, book_pk, chapter_pk):
    if request.method == 'POST':
        chapter = get_object_or_404(Chapter, pk=chapter_pk)
        create_reading_mark(chapter.id, request.user.id)

    return redirect(reverse('book_detail', kwargs={'pk': book_pk}))


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
        return get_object_or_404(
            get_user_model(), username=self.kwargs['username']
        )

    def get_queryset(self):
        user_profile = self.get_user_profile()
        return user_profile.books.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user_profile()
        context['profile'] = user
        context['fully_read_books'] = get_fully_read_books(user)
        context['partially_read_books'] = get_partially_read_books(user)
        return context


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_form.html'
    success_url = reverse_lazy('feedback_thank_you')

    def form_valid(self, form):
        feedback = form.save(commit=False)
        feedback.user = (
            self.request.user if self.request.user.is_authenticated else None
        )
        feedback.save()

        send_mail(
            subject=f"Новая заявка от {feedback.user.username if feedback.user else 'анонимный'}",
            message=feedback.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                settings.FEEDBACK_EMAIL
            ],  # Почта сотрудника для получения заявок
        )
        return super().form_valid(form)


class FeedbackListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Feedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedbacks'


class FeedbackDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Feedback
    template_name = 'feedback/feedback_detail.html'
    context_object_name = 'feedback'

    def post(self, request, *args, **kwargs):
        feedback = self.get_object()
        response = request.POST.get('response')
        feedback.response = response
        feedback.is_responded = True
        feedback.responded_at = timezone.now()
        feedback.save()

        if feedback.user and feedback.user.email:
            send_mail(
                subject='Ответ на вашу заявку',
                message=f'Здравствуйте, {feedback.user.username}!\n\n'
                f'Ваше сообщение: {feedback.message}\n\n'
                f'Ответ от поддержки: {response}\n\n'
                f'С уважением,\nКоманда поддержки.',
                from_email=settings.FEEDBACK_EMAIL,
                recipient_list=[feedback.user.email],
                fail_silently=False,
            )

        return HttpResponseRedirect(f'/feedback/{feedback.pk}/')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_403(request, exception):
    return render(request, '403.html', status=403)


def custom_500(request):
    return render(request, '500.html', status=500)


def custom_400(request, exception):
    return render(request, '400.html', status=400)
