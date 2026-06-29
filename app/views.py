from django.shortcuts import render, redirect
import telebot
from amocrm.v2 import tokens, Lead
from config import TOKEN

from .models import House
tokens.default_token_manager(
    client_id="xxx-xxx-xxxx-xxxx-xxxxxxx",
    client_secret="xxxx",
    subdomain="subdomain",
    redirect_url="https://xxxx/xx",
    storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
)
tokens.default_token_manager.init(code="..very long code...", skip_error=True)



bot = telebot.TeleBot(TOKEN)
group_id = -1003960414454



def home_page(request):
    houses = House.objects.all()
    context = {'houses': houses}
    return render(request,'home.html', context)



def send_form(request):
    if request.method == 'POST':
        parent_name = request.POST.get('parent_name')
        parent_phone = request.POST.get('parent_phone')
        session = request.POST.get('session')
        text = (f'Новый клиент! (Заявка с сайта) \n\n'
                f'Имя родителя: {parent_name}\n'
                f'Номер телефона родителя: {parent_phone}\n'
                f'Смена: {session}')
        #Lead.objects.create(name=parent_name, phone=parent_phone)
        bot.send_message(group_id, text)
    return redirect('/')

def send_form_house(request):
    if request.method == 'POST':
        house_name = request.POST.get('house_name')
        guest_name = request.POST.get('guest_name')
        guest_phone = request.POST.get('guest_phone')
        text = (f'Новый клиент! (Заявка с сайта) \n\n'
                f'Домик: {house_name}\n'
                f'Имя клиента: {guest_name}\n'
                f'Номер телефона: {guest_phone}')
        #Lead.objects.create(house_name=house_name, name=guest_name, phone=guest_phone)
        bot.send_message(group_id, text)
    return redirect('/')