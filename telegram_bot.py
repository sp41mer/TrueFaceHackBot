import datetime
import telegram
from app import bot
from user import User


class TelegramBot:
    start_command = "/start"
    exit_command = "/exit"
    request = dict

    def __init__(self, request):
        self.request = request.json

    @property
    def chat_id(self):
        return self.request['message']['chat']['id']

    @property
    def user_id(self):
        return self.request['message']['from']['id']

    @property
    def message_text(self):
        print(self.request)
        return self.request['message'].get('text')

    @property
    def message_contact(self):
        return self.request['message'].get('contact')

    @property
    def message_photo(self):
        return self.request['message'].get('photo')

    @property
    def minimal_size_photo(self):
        if self.message_photo:
            return self.message_photo[2]['file_id']
        else:
            return None

    @property
    def message_geo(self):
        return self.request['message'].get('location')

    def parse_commands(self):
        if self.message_text == self.start_command:
            print(self.chat_id)
            bot.send_message(chat_id=self.chat_id, text='Send your photo for identification',
                             reply_markup={"hide_keyboard": True})
        if self.minimal_size_photo:
            new_file = bot.get_file(self.minimal_size_photo)
            name, event = User.get_name_by_chat_content(chat_id)
            lat, long = User.get_geo_by_chat_content(chat_id)
            if True:
                print(new_file.file_path)
                bot.send_message(chat_id=self.chat_id, text='Hi {}, upcoming event is '
                                                            '{}'.format(name, event),
                                 reply_markup={"hide_keyboard": True})
                bot.send_location(chat_id=self.chat_id, latitude=lat, longitude=long)
                self.send_help_carousel()
            else:
                bot.send_message(chat_id=self.chat_id,
                                 text='Could not recognize. Send another photo for identification',
                                 reply_markup={"hide_keyboard": True})

        if self.message_geo:
            self.send_get_contacts_carousel()
        if self.message_contact:
            bot.send_message(chat_id=self.chat_id, text='Event organizers will contact and help you',
                             reply_markup={"hide_keyboard": True})
            User.notify_orginizer(self.chat_id)

    @classmethod
    def get_date(cls, date):
        return datetime.datetime.strptime(date.split('T')[0], '%Y-%m-%d').date()

    def send_help_carousel(self):
        custom_keyboard = [
            [
                {"text": "I need help",
                 "request_location": True
                 }
            ],
            ["My events"],
            ["Exit"]
        ]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=self.chat_id,
                         text='Do you need help ?',
                         reply_markup=reply_markup)

    def send_get_contacts_carousel(self, text='How we can contact you ?'):
        custom_keyboard = [
            [
                {"text": "This number",
                 "request_contact": True
                 },
            ],
            [
                {
                    "text": "Number in my profile"
                }
            ]
        ]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=self.chat_id,
                         text=text,
                         reply_markup=reply_markup)