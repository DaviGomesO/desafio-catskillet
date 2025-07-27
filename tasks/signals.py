from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        subject = 'Bem-vindo ao TaskAPI!'
        message = f'Olá {instance.username},\n\nObrigado por usar nosso serviço!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)
