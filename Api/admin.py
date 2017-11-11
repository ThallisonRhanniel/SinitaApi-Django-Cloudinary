from django.contrib import admin
from .models import EventComments
# Register your models here.
class EventCommentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'comment']  # add filter on top of table
    search_fields = ['name', 'comment']  # add a search bar that searches according to the parameters

admin.site.register(EventComments, EventCommentsAdmin)  # add a model in admin

