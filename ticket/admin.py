from django.contrib import admin
from .models import *

# Register your models here.

class CarpetInline(admin.StackedInline):
    model = Carpet
    extra = 1

class TicketAdmin(admin.ModelAdmin):
    inlines = [CarpetInline]

admin.site.register(Ticket, TicketAdmin)
admin.site.register(StatusForTicket)
admin.site.register(StatusForCarpet)
admin.site.register(Client)
admin.site.register(Sale)
admin.site.register(Carpet)
admin.site.register(TicketSaved)
admin.site.register(Services)
