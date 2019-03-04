from django.contrib import admin
from . import models

# Register your models here.

class EntryAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "publish")
    prepopulated_fields = {"slug":("title",)}

class TagAdmin(admin.ModelAdmin):
    list_display = ("tag", "created")

class BlogEntryTagAdmin(admin.ModelAdmin):
    list_display = ("blog_entry", "tag", "created")

admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.BlogEntryTag, BlogEntryTagAdmin)
