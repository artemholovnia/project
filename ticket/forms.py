from django.forms import ModelForm, Form, CharField, IntegerField, NumberInput, TextInput, Textarea, \
    CheckboxInput, Select
from .models import *

class TicketCreateForm(ModelForm):
    class Meta():
        model = Ticket
        fields = ['client','ticket_number', 'phone_number', 'carpets_nmb', 'attentions', 'is_express', 'month']
        widgets = {
            "ticket_number": NumberInput(attrs={'class': 'form-control'}),
            "phone_number": TextInput(attrs={'class': 'form-control'}),
            "carpets_nmb": NumberInput(attrs={'class': 'form-control'}),
            "attentions": Textarea(attrs={'class': 'form-control'}),
            "client": Select(attrs={'class': 'form-control'}),
            "month": Select(attrs={'class': 'form-control'}),
        }
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


