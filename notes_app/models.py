from django.db import models
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

def get_next_day():
    return datetime.now() + timedelta(days=1)

class Note(models.Model):
    class Ratings(models.IntegerChoices):
        active = 1, "Активно"
        delay = 2, "Отложено"
        done = 3, "Выполнено"

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    message = models.TextField(default='', verbose_name="Описание")
    public = models.BooleanField(default=False, verbose_name="Опубликовать")
    importance = models.BooleanField(default=True, verbose_name="Важность")
    condition = models.IntegerField(default=Ratings.active, choices=Ratings.choices, verbose_name="Состояние")
    date_and_time = models.DateTimeField(default=get_next_day, verbose_name="Время создания")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Запись №{self.id}"

    class Meta:
        verbose_name = _("запись")
        verbose_name_plural = _("записи")

