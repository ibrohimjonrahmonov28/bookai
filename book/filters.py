# filters.py
import django_filters
from .models import Participant

class ParticipantFilter(django_filters.FilterSet):
    class Meta:
        model = Participant
        fields = {
            'author__name': ['exact'],
            'book__name': ['icontains'],
        }
