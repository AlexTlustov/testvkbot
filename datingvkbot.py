import vk_api
import re
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from config import user_token, group_token
from random import randrange
from datebase import *

class DatingBot:
    def __init__(self):
        self.user_vk = vk_api.VkApi(token=user_token)
        self.group_vk = vk_api.VkApi(token=group_token)
        self.user_vk_api = self.user_vk.get_api()
        self.group_vk_api = self.group_vk.get_api()
        self.longpoll = VkLongPoll(self.group_vk)

    def _create_user_vk(self, token):
        try:
            return vk_api.VkApi(token=token)
        except vk_api.VkApiError as error:
            print(f"Произошла ошибка при подключении пользователя VkApi: {error}")

    def _create_group_vk(self, token):
        try:
            return vk_api.VkApi(token=token)
        except vk_api.VkApiError as error:
            print(f"Произошла ошибка при подключении группы VkApi: {error}")
    
    def send_message(self, user_id, message):
        try:
            self.group_vk_api.messages.send(
                user_id=user_id,
                message=message,
                random_id=randrange(10 ** 7)
            )
        except vk_api.VkApiError as error:
            print(f"Произошла ошибка при отправке сообщения: {error}")

    def get_user_info(self, user_id):
        try:
            user_info = self.group_vk_api.users.get(user_id=user_id)
            name = user_info[0]['first_name']
            return name
        except (KeyError, vk_api.VkApiError) as error:
            print(f"Произошла ошибка при получении информации о пользователе: {error}")

    def declination_of_years(self, year):
        exception = [11, 12, 13, 14]
        if year % 10 == 1 and year not in exception:
            return f'{year} год.'
        elif year % 10 == 2 and year not in exception:
            return f'{year} года.'
        elif year % 10 == 3 and year not in exception:
            return f'{year} года.'
        elif year % 10 == 4 and year not in exception:
            return f'{year} года.'
        else:
            return f'{year} лет.'
        
    def search_enter_age(self, user_id, age: str):
        global age_from, age_to
        pattern = r'\d+'
        age_list = []
        for element in age.split():
            if re.match(pattern, str(element)):
                age_list.append(element)
        try:
            age_from = int(age_list[0])
            age_to = int(age_list[1])
            if age_from == age_to:
                self.send_message(user_id, f'Поиск пользователей в возрасте {self.declination_of_years(age_to)}')
                return
            self.send_message(user_id, f' Поиск пользователей в возрасте от {age_from} и до {self.declination_of_years(age_to)}')
            return
        except IndexError as error:
            age_to = int(age)
            self.send_message(user_id, f'Поиск пользователей в возрасте {self.declination_of_years(age_to)}')
            return
        except NameError as error:
            self.send_message(user_id, f'Возникла ошибка {error}. Укажити возраст в формате: "от <число> до <число>"')
            return
        except ValueError as error:
            self.send_message(user_id, f'Возникла ошибка {error}. Укажити возраст в формате: "от <число> до <число>"')
            return
    
    def get_person_age(self, bdate: str):
        month_dict = {
        '1': 'января',
        '2': 'февраля',
        '3': 'марта',
        '4': 'апреля',
        '5': 'мая',
        '6': 'июня',
        '7': 'июля',
        '8': 'августа',
        '9': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря'
        }
        try:    
            bdate_split = bdate.split('.')
            month = ''
            rev_bdate = datetime.date(int(bdate_split[2]), int(bdate_split[1]), int(bdate_split[0]))
            today = datetime.date.today()
            years = today.year - rev_bdate.year
            if rev_bdate.month == today.month and rev_bdate.day <= today.day or rev_bdate.month < today.month:
                years -= 1
            return self.declination_of_years(years)
        except IndexError:
            month = month_dict.get(bdate_split[1])
            day = int(bdate_split[0])
            return f'День рождения {day} {month}.' if month else None
            
    
    def get_user_age(self, user_id):
        global age_from, age_to
        try:
            information = self.user_vk_api.users.get(
                user_ids=user_id,
                fields='bdate',
            )[0]['bdate']
            user_age = self.get_person_age(information).split()[0]
            age_from = user_age
            age_to = user_age
            if user_age == 'День':
                self.send_message(user_id,
                              f'   Я не знаю Ваш возраст потому что вы скрыли год рождения в настройках приватности. \n'
                              f'   Поэтому придется использовать руки. Укажити возраст в формате: "от <число> до <число>" '
                              )
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return self.search_enter_age(user_id, age)
            return self.declination_of_years(age_to)
        except KeyError:
            self.send_message(user_id,
                          f' Я не знаю Ваш возраст потому что вы скрыли год рождения в настройках приватности. '
                          f'\n Поэтому придется использовать руки. Укажити возраст в формате: "от <число> до <число>"'
                          )
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    return self.search_enter_age(user_id, age)
                
    def get_city(self, user_id):
        global city_id, city_title
        self.send_message(user_id,
                      f'Введите "Да" - будем искать в городе указанный в Вашем профиле.'
                      f'Введите <город> - будем искать в городе который Вы скажете. Например: Москва'
                      )
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                answer = event.text.lower()
                if answer == "да":
                    info = self.user_vk_api.users.get(
                        user_id=user_id,
                        fields="city"
                    )
                    city_id = info[0]['city']["id"]
                    city_title = info[0]['city']["title"]
                    return f'В городе {city_title}.'
                else:
                    cities = self.user_vk_api.database.getCities(
                        country_id=1,
                        q=answer.capitalize(),
                        need_all=1,
                        count=1000
                    )['items']
                    for i in cities:
                        if i["title"] == answer.capitalize():
                            city_id = i["id"]
                            city_title = answer.capitalize()
                            return f'В городе {city_title}'

    def get_search_gender(self, user_id):
        information = self.user_vk_api.users.get(
            user_id=user_id,
            fields='sex'
        )
        user_gender = information[0]['sex']
        if user_gender == 1: 
            print(f'Ваш пол женский, ищем мужчину.')
            return 2
        elif user_gender == 2:
            print(f'Ваш пол мужской, ищем женщину.')
            return 1
        else:
            print("ERROR!!!")

    def looking_for_persons(self, user_id):
        global list_found_persons
        list_found_persons = []
        res = self.user_vk_api.users.search( 
            sort=0,  
            city=city_id,
            hometown=city_title,
            sex=self.get_search_gender(user_id),  
            status=1,  
            age_from=age_from,
            age_to=age_to,
            has_photo=1,  
            count=1000,
            fields="can_write_private_message, "  
                   "city, "  
                   "domain, "  
                   "home_town, "  
        )
        number = 0
        for person in res["items"]:
            if not person["is_closed"]:
                if "city" in person and person["city"]["id"] == city_id and person["city"]["title"] == city_title:
                    number += 1
                    id_vk = person["id"]
                    list_found_persons.append(id_vk)
        print(f'Я нашел {number} доступных анкет из {res["count"]}')
        return
    
    def photos_found_users(self, user_id):
        global attachments
        attachments = []
        res = self.user_vk_api.photos.get(
            owner_id=user_id,
            album_id="profile",  
            extended=1,  
            count=30
        )
        dict_photos = {}
        for i in res['items']:
            photo_id = str(i["id"])
            i_likes = i["likes"]
            if i_likes["count"]:
                likes = i_likes["count"]
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        photo_ids = []
        for i in list_of_ids:
            photo_ids.append(i[1])
        try:
            attachments.append('photo{}_{}'.format(user_id, photo_ids[0]))
            attachments.append('photo{}_{}'.format(user_id, photo_ids[1]))
            attachments.append('photo{}_{}'.format(user_id, photo_ids[2]))
            return attachments
        except IndexError:
            try:
                attachments.append('photo{}_{}'.format(user_id, photo_ids[0]))
                return attachments
            except IndexError:
                return print(f'Нет фото')
            
    def found_person_info(self, show_person_id):
        res = self.user_vk_api.users.get(
            user_ids=show_person_id,
            fields="about, "  # Поле «О себе»
                   "activities, "  # Поле «Деятельность».
                   "bdate, "  # Дата рождения. Если дата рождения скрыта, поле отсутствует в ответе.
                   "status, "
                   "can_write_private_message, "  # Информация о том, может ли текущий пользователь отправить личное сообщение. Возможные значения: 1 — может; 0 — не может.
                   "city, "  # Город из раздела контакты.
                   "common_count, "  # Количество общих друзей.
                   "contacts, "  # Информация о телефонных номерах пользователя.
                   "domain, "  # Короткий адрес страницы.
                   "home_town, "  # Родной города.
                   "interests, "  # Поле «Интересы».
                   "movies, "  # Поле «Любимые фильмы».
                   "music, "  # Поле «Любимая музыка».
                   "occupation"  # Информация о занятиях пользователя.
        )
        first_name = res[0]["first_name"]
        last_name = res[0]["last_name"]
        age = self.get_person_age(res[0]["bdate"])
        vk_link = 'vk.com/' + res[0]["domain"]
        city = ''
        try:
            if res[0]["city"]["title"] is not None:
                city = f'Город {res[0]["city"]["title"]}'
            else:
                city = f'Город {res[0]["home_town"]}'
        except KeyError:
            pass
        print(f'{first_name} {last_name}, {age}, {city}. {vk_link}')
        return f'{first_name} {last_name}, {age}, {city}. {vk_link}'

    def send_photo(self, user_id, message, attachments):
        try:
            self.group_vk_api.messages.send(
                user_id=user_id,
                message=message,
                random_id=randrange(10 ** 7),
                attachment=",".join(attachments)
            )
        except TypeError:
            pass

    def get_person_from_db(self):
        global unique_person_id, found_persons
        seen_person = []
        for i in check():  # Выбираем из БД просмотренные анкеты.
            seen_person.append(int(i[0]))
        if not seen_person:
            try:   # Если сразу после запуска проги набрать Смотреть или S, то ошибка так как в list_found_persons никого нет.
                unique_person_id = list_found_persons[0]
                return unique_person_id
            except NameError:
                found_persons = 0
                return found_persons
        else:
            try:  # Если сразу после запуска проги набрать Смотреть или S, то ошибка так как в list_found_persons никого нет.
                for ifp in list_found_persons:
                    if ifp in seen_person:
                        pass
                    else:
                        unique_person_id = ifp
                        return unique_person_id
            except NameError:
                found_persons = 0
                return found_persons
    
    def show_found_person(self, user_id):
        print(self.get_person_from_db())
        if self.get_person_from_db() == None:
            self.send_message(user_id,
                          f'Все анекты ранее были просмотрены. Будет выполнен новый поиск. '
                          f'Измените критерии поиска (возраст, город). '
                          f'Введите возраст поиска, на пример от 21 года и до 35 лет, '
                          f'в формате : 21-35 (или 21 конкретный возраст 21 год).  ')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age = event.text
                    self.search_enter_age(user_id, age)
                    self.get_city(user_id)
                    self.looking_for_persons(user_id)
                    self.show_found_person(user_id)
                    return
        else:
            self.send_message(user_id, self.found_person_info(self.get_person_from_db()))
            self.send_photo(user_id, 'Фото с максимальными лайками',
                            self.photos_found_users(self.get_person_from_db()))
            insert_data_seen_person(self.get_person_from_db())

datingbot = DatingBot()