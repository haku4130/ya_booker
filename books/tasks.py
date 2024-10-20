from django.contrib.auth import get_user_model
from django.db.models import Count, Q, F

from .models import ReadingMark, Chapter, Book


def create_reading_mark(chapter_id, user_id):
    chapter = Chapter.objects.get(id=chapter_id)
    user = get_user_model().objects.get(id=user_id)
    ReadingMark.objects.create(chapter=chapter, user=user)


def get_fully_read_books(user):
    # Получаем книги, для которых количество глав равно количеству отметок о прочтении для данного пользователя
    fully_read_books = Book.objects.annotate(
        total_chapters=Count('chapters'),
        read_chapters=Count(
            'chapters__read_marks', filter=Q(chapters__read_marks__user=user)
        ),
    ).filter(read_chapters__gt=0, total_chapters=F('read_chapters'))

    return fully_read_books.order_by('id')


def get_partially_read_books(user):
    # Аннотация книг с количеством глав и количеством прочитанных глав пользователем
    partially_read_books = Book.objects.annotate(
        total_chapters=Count('chapters'),  # Общее количество глав в книге
        read_chapters=Count(
            'chapters__read_marks', filter=Q(chapters__read_marks__user=user)
        ),  # Количество прочитанных глав
    ).filter(
        read_chapters__gt=0, read_chapters__lt=F('total_chapters')
    )  # Условия: прочитано > 0, но < общего числа глав

    return partially_read_books.order_by('id')


def get_reading_users(book):
    return (
        get_user_model()
        .objects.filter(reading_marks__chapter__book=book)
        .annotate(read_chapters=Count('reading_marks__chapter', distinct=True))
        .filter(
            read_chapters__gt=0,
            read_chapters__lt=book.chapters.count(),  # Сравниваем с количеством глав в книге
        )
    )


def get_completed_users(book):
    return (
        get_user_model()
        .objects.filter(reading_marks__chapter__book=book)
        .annotate(read_chapters=Count('reading_marks__chapter', distinct=True))
        .filter(
            read_chapters=book.chapters.count()
        )  # Количество прочитанных глав должно равняться общему числу глав
    )
