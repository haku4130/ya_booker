from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)

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
        return f"{self.book.title} - {self.title}"


class ReadingMark(models.Model):
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name='read_marks'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reading_marks',
    )
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} read {self.chapter.title} at {self.marked_at}"
