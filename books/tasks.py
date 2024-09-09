from celery import shared_task
from django.contrib.auth.models import User
from .models import ReadingMark, Chapter


@shared_task
def create_reading_mark(chapter_id, user_id):
    chapter = Chapter.objects.get(id=chapter_id)
    user = User.objects.get(id=user_id)
    ReadingMark.objects.create(chapter=chapter, user=user)
