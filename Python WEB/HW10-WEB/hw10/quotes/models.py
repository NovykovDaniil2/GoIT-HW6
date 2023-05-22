from django.db import models


class Tag(models.Model):
    name = models.CharField(null=False, unique=True)


class Author(models.Model):
    fullname = models.CharField(null=False, unique=True)
    born_date = models.CharField()
    born_location = models.CharField()
    biography = models.TextField()


class Quote(models.Model):
    quote = models.CharField()
    author = models.ManyToManyField(Author)
    tags = models.ManyToManyField(Tag)
    publication_date = models.DateTimeField(auto_now_add=True)

