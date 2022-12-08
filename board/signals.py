from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Ad


@receiver(post_save, sender=Ad)
def notify_post_create(sender, instance, created, *args, **kwargs):
    recipient = []
    for user in User.objects.all():
        recipient.append(user.email)
    if created:
        send_mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=f'{instance.author.username} create {instance.title} with text {instance.text} '
                    f'in category {instance.category}',
            recipient_list=[*recipient],
            subject='New post!'
        )
