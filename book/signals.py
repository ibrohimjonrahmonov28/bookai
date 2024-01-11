from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.db import models

from yourapp.models import Favorite  # Replace 'yourapp' with the actual name of your app

@receiver(post_save, sender=Favorite)
def update_favorite_books_cache(sender, instance, created, **kwargs):
    if created:
        cache_key = f"favorite_book_{instance.user.id}"
        cache.delete(cache_key)
