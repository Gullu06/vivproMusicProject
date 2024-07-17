from django.contrib import admin # type: ignore
from .models import Song

# Register your models here.
admin.site.register(Song)
