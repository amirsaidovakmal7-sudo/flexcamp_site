from django.shortcuts import render, redirect
import telebot
from amocrm.v2 import tokens, Lead
from config import TOKEN

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
    return render(request,'home.html')



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

