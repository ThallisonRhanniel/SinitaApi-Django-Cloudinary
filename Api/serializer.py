from cloudinary.templatetags import cloudinary
from rest_framework import serializers
from .models import EventComments
from django.contrib.humanize.templatetags.humanize import naturaltime
import cloudinary
import cloudinary.uploader
import cloudinary.api


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventComments
        fields = ('id', 'name', 'icon_perfil', 'category', 'comment', 'created')  # __all__

    def to_representation(self, instance):
        representation = super(CommentSerializer, self).to_representation(instance)
        icon_perfil_url = cloudinary.utils.cloudinary_url(instance.icon_perfil, width=100, height=150,
                                                          crop="fill", quality="30")
        representation['icon_perfil'] = icon_perfil_url[0]
        representation['created'] = naturaltime(instance.created)
        return representation
