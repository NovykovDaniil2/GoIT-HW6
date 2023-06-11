from django.contrib import admin
from .models import Quote, Tag, Author


admin.site.register(Quote)
admin.site.register(Tag)
admin.site.register(Author)