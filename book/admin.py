from django.contrib import admin

from .models import Category,Book,BookViews,Participant,Rating,Comment, AudioFile


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'isbn_number', 'price')  # Ko'rsatiladigan ustunlar
    search_fields = ('id', 'name', 'isbn_number', 'price')  # Izlash uchun ustunlar

admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(BookViews)
admin.site.register(Participant)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(AudioFile)
