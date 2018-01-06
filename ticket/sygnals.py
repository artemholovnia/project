from .models import Ticket
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Carpet)
def add_ready_carpets(sender, instance, **kwargs):
    carpets_ready_nmb = Carpet.ticket.carpets_ready_nmb
    print(carpets_ready_nmb)