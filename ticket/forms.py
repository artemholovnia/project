from django.forms import ModelForm, Form, CharField, IntegerField
from .models import *

class TicketCreateForm(ModelForm):
    class Meta():
        model = Ticket
        fields = ['client','ticket_number', 'phone_number', 'carpets_nmb', 'attentions', 'is_express', 'month']

class CarpetCreateForm(ModelForm):
    class Meta():
        model = Carpet
        fields = ['height', 'width', 'neutralization', 'ozon', 'impregnation', 'roztocz', 'siersc']


class CarpetUpdateForm(ModelForm):
    class Meta():
        model = Carpet
        fields = ['height', 'width', 'neutralization', 'ozon', 'impregnation', 'roztocz', 'siersc', 'status']

class FindForm(Form):
    find_text = CharField(max_length=20, label='find')

class CoastTicketForm(Form):
    coast = IntegerField(max_value=9999, label='Cena')
    sale = IntegerField(max_value=100, label='Zniżka')


