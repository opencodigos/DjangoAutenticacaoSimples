from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from accounts.models import CustomUser

class MyProfile(models.Model):
    user = models.OneToOneField(CustomUser, 
						on_delete=models.CASCADE, related_name='profile')
    description = models.CharField(max_length=100)


@receiver(post_save, sender=CustomUser)
def my_handler(sender, **kwargs):
    """
    Quando Criar um usuário no Django, vai rodar essa função
    para criar uma instancia nesse modelo MyProfile no campo "user".
    """
    if kwargs.get('created', False):
        MyProfile.objects.create(user=kwargs['instance'])