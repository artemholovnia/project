from django.forms import Form, IntegerField, CharField, TextInput, NumberInput

class OrderVerificationForm(Form):
    order_number = IntegerField(label='order_number', help_text='Wpisz numer zamwienia',
                                widget=NumberInput(attrs={'class':'form-control'}))
    phone_number = CharField(label='phone_number', help_text='Wpisz numer telefonu dodany do zamówienia',
                             widget=TextInput(attrs={'class':'form-control'}))