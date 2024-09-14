from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    ChapterCreateView,
    BookUpdateView,
    BookDeleteView,
    ProfileListView,
    create_reading_mark_view,
)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path(
        'books/<int:pk>/add-chapter/',
        ChapterCreateView.as_view(),
        name='chapter_create',
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
]
