from django.db import models
from cloudinary.models import CloudinaryField
# Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel  # django-model-utils
from rest_framework.authtoken.models import Token


# class MyPhoto(models.Model):
#     name = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='myphoto/%Y/%m/%d/', null=True, max_length=255)
#     #doc = models.FileField(upload_to='Doc/', default='Doc/None/nodc.pdf')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class EventComments(TimeStampedModel):
    name = models.CharField(max_length=25, verbose_name='Name')
    icon_perfil = models.CharField(max_length=100, verbose_name='Icon_Perfil')
    category = models.CharField(max_length=15, verbose_name='Category')
    comment = models.CharField(max_length=250, verbose_name='Comment')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Event Coment'
        verbose_name_plural = 'Event Coments'
        ordering = ['-created']
