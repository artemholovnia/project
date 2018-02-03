from django.shortcuts import get_list_or_404
from .models import *
import openpyxl
from openpyxl.styles import Alignment
from openpyxl.drawing.image import Image
import os
from django.utils.timezone import datetime
import pathlib

services = Services.objects.get(id=1)
COAST_PER_M = services.per_m
COAST_N = services.neutralization
COAST_I = services.impregnation
COAST_O = services.ozon
COAST_R = services.roztocz
COAST_S = services.siersc
COAST_EXSPRESS = services.express

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, 'static/media/tickets_docs/' + datetime.today().strftime('%d-%m-%Y'))
pathlib.Path(PATH).mkdir(parents=True, exist_ok=True)
POSITIONS = {
    'ticket_number': 'J1',
    'logo': 'B2',
    'created': 'D8',
    'ended': 'J8',
    'phone_number': 'D9',
    'address': 'D10',
    'carpet_size': 'C/12',
    'carpet_attentions': 'D/12',
    'carpet_n': 'E/12',
    'carpet_o': 'F/12',
    'carpet_i': 'G/12',
    'carpet_s': 'H/12',
    'carpet_r': 'I/12',
    'carpet_coast': 'J/12',
    'ticket_coast': 'J24',

}

def generate_ticket_document(ticket_identificator):
    img = Image(os.path.join(BASE_DIR, 'static/media/tickets_docs/logo.jpg'))
    itteration = 0
    ticket = Ticket.objects.get(identificator=ticket_identificator)
    carpets = get_list_or_404(Carpet, ticket=ticket)
    path = os.path.join(BASE_DIR, 'static/media/tickets_docs')
    workbook = openpyxl.load_workbook(path + '/ticket_template.xlsx')
    work_sheet = workbook.get_sheet_by_name('ticket_template')
    work_sheet.title = 'generated_ticket'
    #paste logo
    work_sheet.add_image(img, POSITIONS.get('logo'))
    #paste data
    work_sheet.add_image(img)
    work_sheet[POSITIONS.get('created')] = ticket.created.strftime('%d-%m-%Y')
    work_sheet[POSITIONS.get('ended')] = '-'
    work_sheet[POSITIONS.get('phone_number')] = ticket.phone_number
    work_sheet[POSITIONS.get('address')] = ticket.address
    work_sheet[POSITIONS.get('ticket_coast')] = str(ticket.coast) + ' zł'
    work_sheet[POSITIONS.get('ended')] = datetime.today().strftime('%d-%m-%Y')
    work_sheet[POSITIONS.get('ticket_number')] = ticket.ticket_number
    for carpet in carpets:
        carpet_per_m = COAST_PER_M
        carpet_coast = 0
        itteration += 1

        carpet_size_pos = POSITIONS.get('carpet_size').split('/')
        carpet_size_pos_paste = carpet_size_pos[0] + str(int(carpet_size_pos[1]) + itteration)
        work_sheet[carpet_size_pos_paste] = str(carpet.height) + '*' + str(carpet.width)

        carpet_attentions_pos = POSITIONS.get('carpet_attentions').split('/')
        carpet_attentions_pos_paste = carpet_attentions_pos[0] + str(int(carpet_attentions_pos[1]) + itteration)
        work_sheet[carpet_attentions_pos_paste] = '-'
        if ticket.is_express:
            carpet_per_m *= COAST_EXSPRESS
        if carpet.neutralization:
            carpet_per_m += COAST_N
            carpet_n_pos = POSITIONS.get('carpet_n').split('/')
            carpet_n_pos_paste = carpet_n_pos[0] + str(int(carpet_n_pos[1]) + itteration)
            work_sheet[carpet_n_pos_paste] = '+'

        if carpet.ozon:
            carpet_coast += COAST_O
            carpet_o_pos = POSITIONS.get('carpet_o').split('/')
            carpet_o_pos_paste = carpet_o_pos[0] + str(int(carpet_o_pos[1]) + itteration)
            work_sheet[carpet_o_pos_paste] = '+'

        if carpet.impregnation:
            carpet_per_m += COAST_I
            carpet_i_pos = POSITIONS.get('carpet_i').split('/')
            carpet_i_pos_paste = carpet_i_pos[0] + str(int(carpet_i_pos[1]) + itteration)
            work_sheet[carpet_i_pos_paste] = '+'

        if carpet.siersc:
            carpet_per_m += COAST_S
            carpet_s_pos = POSITIONS.get('carpet_s').split('/')
            carpet_s_pos_paste = carpet_s_pos[0] + str(int(carpet_s_pos[1]) + itteration)
            work_sheet[carpet_s_pos_paste] = '+'

        if carpet.roztocz:
            carpet_per_m += COAST_R
            carpet_r_pos = POSITIONS.get('carpet_r').split('/')
            carpet_r_pos_paste = carpet_r_pos[0] + str(int(carpet_r_pos[1]) + itteration)
            work_sheet[carpet_r_pos_paste] = '+'

        carpet_coast += carpet.height * carpet.width * carpet_per_m
        if ticket.is_express:
            carpet_coast *= COAST_EXSPRESS
        carpet_coast_pos = POSITIONS.get('carpet_coast').split('/')
        carpet_coast_pos_paste = carpet_coast_pos[0] + str(int(carpet_coast_pos[1]) + itteration)
        work_sheet[carpet_coast_pos_paste] = str(carpet_coast) + ' zł'



    ticket_number = ticket.ticket_number.split('/')
    ticket_saving_number = ticket_number[0] + '.' + ticket_number[1]

    name_to_save = '/ticket_' + ticket_saving_number + '_' + ticket.created.strftime('%d-%m-%Y') + '.xlsx'
    workbook.save(PATH + name_to_save)

    try:
        ticket_saved = TicketSaved.objects.get(ticket_identificator=ticket_identificator)
        ticket_saved.delete()
        ticket_saved = TicketSaved.objects.create(path=PATH, file_name=name_to_save,
                                                  ticket_identificator=ticket_identificator)
        ticket_saved.save()

    except TicketSaved.DoesNotExist:
        ticket_saved = TicketSaved.objects.create(path=PATH, file_name=name_to_save,
                                                  ticket_identificator=ticket_identificator)
        ticket_saved.save()
    return True
