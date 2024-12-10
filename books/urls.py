from django.urls import path
from django.views.generic import TemplateView

from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    ChapterCreateView,
    ChapterUpdateView,
    BookUpdateView,
    BookDeleteView,
    ProfileListView,
    create_reading_mark_view,
    FeedbackCreateView,
    FeedbackListView,
    FeedbackDetailView,
)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path(
        'books/<int:pk>/update/', BookUpdateView.as_view(), name='book_update'
    ),
    path(
        'books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'
    ),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path(
        'books/<int:pk>/add-chapter/',
        ChapterCreateView.as_view(),
        name='chapter_create',
    ),
    path(
        'books/<int:pk>/update-chapter/<int:chapter_pk>/',
        ChapterUpdateView.as_view(),
        name='chapter_update',
    ),
    path(
        'books/<int:book_pk>/chapters/<int:chapter_pk>/mark/',
        create_reading_mark_view,
        name='reading_mark_create',
    ),
    path(
        'profile/<str:username>/',
        ProfileListView.as_view(),
        name='profile',
    ),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback_form'),
    path(
        'feedback/thank-you/',
        TemplateView.as_view(template_name='feedback/feedback_thank_you.html'),
        name='feedback_thank_you',
    ),
    path('feedback/list/', FeedbackListView.as_view(), name='feedback_list'),
    path(
        'feedback/<int:pk>/',
        FeedbackDetailView.as_view(),
        name='feedback_detail',
    ),
]
