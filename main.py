from vk_api.longpoll import VkEventType, VkLongPoll
from datingvkbot import *
from config import *


for event in datingbot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = event.user_id
        if request == 'поиск' or request == 'f':
            datingbot.get_user_age(user_id)
            datingbot.get_city(user_id)
            datingbot.looking_for_persons(user_id)  # выводит список в чат найденных людей и добавляет их в базу данных.
            datingbot.show_found_person(user_id)  # выводит в чат инфо одного человека из базы данных.
        elif request == 'удалить' or request == 'd':
            delete_table_seen_person()  # удаляет существующую БД.
            create_table_seen_person()  # создает новую БД.
            datingbot.send_message(user_id, f' База данных отчищена! Сейчас наберите "Поиск" или F ')
        elif request == 'смотреть' or request == 's':
            if datingbot.get_person_from_db() != 0:
                datingbot.show_found_person(user_id)
            else:
                datingbot.send_message(user_id, f' В начале наберите Поиск или f.  ')
        else:
            datingbot.send_message(user_id, f'{datingbot.get_user_info(user_id)} Бот готов к поиску, наберите: \n '
                                      f' "Поиск или F" - Поиск людей. \n'
                                      f' "Удалить или D" - удаляет старую БД и создает новую. \n'
                                      f' "Смотреть или S" - просмотр следующей записи в БД.')