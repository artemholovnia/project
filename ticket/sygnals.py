from .models import Carpet
from record.models import Record
from django.db.models.signals import post_save
from django.dispatch import receiver


#create or update record
@receiver(post_save, sender=Carpet)
def save_record(sender, instance, **kwargs):
    print('its work')