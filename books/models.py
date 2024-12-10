from django.db import models
from django.contrib.auth import get_user_model


class Book(models.Model):
    title = models.CharField(max_length=255)
    added_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='books',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='chapters'
    )
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.book.title} - {self.title}'


class ReadingMark(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name='read_marks'
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='reading_marks',
    )
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} read {self.chapter.title} at {self.marked_at}'


class Feedback(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)
    response = models.TextField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Заявка от {self.user.username if self.user else 'анонимный'} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']
