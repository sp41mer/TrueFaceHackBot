import datetime
import telegram
from app import bot


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
        # Если только начали
        if self.message_text == self.start_command:
            bot.send_message(chat_id=self.chat_id, text='Send your photo for identification',
                             reply_markup={"hide_keyboard": True})
        if self.minimal_size_photo:
            new_file = bot.get_file(self.minimal_size_photo)
            # Вот тут идем в апиху и берем Имя
            if True:
                print(new_file.file_path)
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

    @classmethod
    def get_date(cls, date):
        return datetime.datetime.strptime(date.split('T')[0], '%Y-%m-%d').date()

    def send_help_carousel(self, text='Alex'):
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
                         text='Hi, {}! \nDo you need help ?'.format(text),
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

MAP, CONTACT = 1, 2
redis_structure = {
    "chat_id": '1223',
    "user_id": '12',
    "help_activated": True,
    "help_step": MAP
}
