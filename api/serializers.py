from rest_framework import serializers
from ticket.models import *

class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('__all__')

class CarpetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpet
        fields = ('__all__')
