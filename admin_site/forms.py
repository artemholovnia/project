from django.forms import Form, ModelForm, TextInput, Select, CheckboxInput, NumberInput, CharField
from ticket.models import Worker
from django.contrib.auth.forms import User, UserCreationForm

class CreateWorkerForm(ModelForm):
    class Meta:
        model = Worker
        exclude = ['status']
        widgets = {
            'user': Select(attrs={'class': 'form-control'}),
            'position': Select(attrs={'class': 'form-control'}),
            'permission': NumberInput(attrs={'class': 'form-control'}),
        }

class CreateUserForm(Form):
    username = CharField(max_length=32, widget=TextInput(attrs={'class': 'form-control'}))
    password = CharField(max_length=16, widget=TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    repeat_password = CharField(max_length=16, widget=TextInput(attrs={'class': 'form-control', 'type': 'password'}))