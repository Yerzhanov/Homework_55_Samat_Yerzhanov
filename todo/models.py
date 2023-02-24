from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextChoices
from django.utils import timezone


class StatusChoice(TextChoices):
    ACTIVE = 'ACTIVE', 'Активна'
    NOT_ACTIVE = 'NOT_ACTIVE', 'Неактивна'


class Todolist(models.Model):
    status = models.CharField(max_length=20, verbose_name='Статус', choices=StatusChoice.choices, default=StatusChoice.ACTIVE)
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(verbose_name='удалено', null=False, default=False)
    date_deleted = models.DateTimeField(null=True, blank=True, default=None)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.date_deleted = timezone.now()
        self.save()



