from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_account(sender, instance=None, created=False, **kwargs):
    if created:
        Account.objects.create(user=instance)
