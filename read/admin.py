from django.contrib import admin

# Register your models here.
from .models import Genre,Book,library_book,Chapter,Reading_list,Reading_Progress

admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(library_book)
admin.site.register(Chapter)
admin.site.register(Reading_list)
admin.site.register(Reading_Progress)