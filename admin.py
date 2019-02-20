from django.contrib import admin
from . import models

# Register your models here.

class EntryAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "publish")
    prepopulated_fields = {"slug":("title",)}

admin.site.register(models.Entry, EntryAdmin)
