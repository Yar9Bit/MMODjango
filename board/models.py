from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='Название объявления')
    text = models.TextField(verbose_name='Текст объявления')
    CATS = (
        ('tanks', 'Танки'),
        ('heals', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('givers', 'Квестгиверы'),
        ('smiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potions', 'Зельевары'),
        ('spellcasters', 'Мастера заклинаний')
    )
    category = models.CharField(max_length=12, choices=CATS, default='tanks', verbose_name='Категория')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    attach = models.FileField(upload_to='uploads/%Y/%m/%d', blank=True, null=True, verbose_name='Вложение')

    class Meta:
        verbose_name = 'Объявление'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.pk)])


class Resp(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    post = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    text = models.TextField(verbose_name='Текст отклика')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отклика')
    status = models.BooleanField(default=False, verbose_name='Статус')

    class Meta:
        verbose_name = 'Отклик'

    def __str__(self):
        return self.text[:64]
