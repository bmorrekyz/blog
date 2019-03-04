from django.db import models
from django_markup.fields import MarkupField

# Create your models here.

class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)

class Entry(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    markup = MarkupField(default='markdown')

    objects = EntryQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries"
        ordering = ["-created"]

class Tag(models.Model):
    tag = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "Tag Name"
        verbose_name_plural = "Tag Names"
        ordering = ["-created"]

class BlogEntryTag(models.Model):
    blog_entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Blog Entry Tag"
        verbose_name_plural = "Blog Entry Tags"
        ordering = ["-blog_entry", "-tag"]
