from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category,Book,BookViews,Participant
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BookViews)
admin.site.register(Participant)
