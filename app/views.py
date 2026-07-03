from django.shortcuts import render, redirect
import telebot
import os
from amocrm.v2 import tokens, Lead
from config import TOKEN
from . models import Comments

print('1. Запуск')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Сохраняем токены в: {BASE_DIR}")


# tokens.default_token_manager(
#     client_id="e9a129fe-7c84-4f9e-9bbc-5ce01612a78c",
#     client_secret="x7PDJ0G3ojUkov7gkocuJtiALEhfZ5f2TQXOnm90f0YExS5z5cRvpmwGVEHA7ZPd",
#     subdomain="muslimpulatov0317",
#     redirect_url="https://flexcamp.uz",
#     storage=tokens.FileTokensStorage(directory_path=BASE_DIR),  # by default FileTokensStorage
# )


print("2. Менеджер настроен")




bot = telebot.TeleBot(TOKEN)
group_id = -1003960414454



def home_page(request):
    comments = Comments.objects.all()
    context = {'comments': comments}
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

