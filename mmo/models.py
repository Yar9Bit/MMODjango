from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Танки, Хилы, ДД, Торговцы, Гилдмастеры, Квестгиверы, Кузнецы, Кожевники, Зельевары, Мастера заклинаний


class Category(models.Model):
    TANK = 'TK'
    HEAL = 'HL'
    DD = 'DD'
    BUY = 'B'
    GILDMASTER = 'GD'
    QUESTGIVER = 'QG'
    SMITH = 'S'
    TANNER = 'T'
    POTION_MASTER = 'PM'
    SPELL_MASTER = 'SM'
    CATEGORY_CHOICES = [
        (TANK, 'Танк'),
        (HEAL, 'Хил'),
        (DD, 'ДД'),
        (BUY, 'Торговцы'),
        (GILDMASTER, 'Гилдмастер'),
        (QUESTGIVER, 'Квестгивер'),
        (SMITH, 'Кузнец'),
        (TANNER, 'Кожевник'),
        (POTION_MASTER, 'Зельевар'),
        (SPELL_MASTER, 'Мастер заклинаний'),
    ]
    name = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=None)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Ad(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    poster = models.FileField("Постер", upload_to='ad_storage/')
    text = models.TextField()

    def get_absolute_url(self):
        return reverse('ad_detail', args=[self.id])

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    photo = models.FileField("Изображение", upload_to='ad_storage/')


class Comment(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    email = models.EmailField(default='user@example.com')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.author} <-> {self.ad}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
