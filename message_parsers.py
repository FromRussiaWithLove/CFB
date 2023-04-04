import re

from db_handler_selector import DbHandlerSelector
import datetime_methods


class MessageParser:

    def __init__(self, message):
        self.__message_type = None
        self.__content = ''
        self.__volume = 0
        self.__breast = False
        self.__timestamp = message.date
        self.__child_id = None
        self.__parse_message(message)

    def __parse_message(self, message):
        db_handler = DbHandlerSelector.get_db_handler()

        message_list = message.text.lower().split()
        # Если длина сообщения 1 слово и оно является псевдонимом
        # то это запрос таблицы кормлений
        if len(message_list) == 1:
            child = db_handler.get_child_from_pseudo(message_list[0])
            if not child is None:
                self.__message_type = 'feed_request'
                self.__child_id = child
                return
        # Если сообщение начинается с sql то это запрос к бд
        elif message_list[0] == 'sql':
            self.__message_type = 'sql_request'
            self.__content = message.text.lower().replace('sql ', '')
            return
        addition_content = ''
        # Проходим по соообщению
        for item in message_list:
            # Если элемент соответствует времени, то устанавливаем новое время
            if re.fullmatch(r'\d{1,2}.\d\d', item):
                self.__timestamp = datetime_methods.timestamp_from_time(message.date, item)
                continue

            if item == 'с' and not self.__breast:
                self.__breast = True
                continue

            # Если элемент это число, то это объем кормления
            if re.fullmatch(r'\d{1,3}', item):
                self.__content += f'{item}мл '
                continue

            # Если элемент соответствует псевдониму, то устанавливаем псевдоним
            child = db_handler.get_child_from_pseudo(item)
            if not child is None:
                self.__child_id = child
                continue

            addition_content += f' {item}'
        self.__content += addition_content
        if self.__breast:
            self.__content = 'C ' + self.__content
        if self.content != '' and not self.__child_id is None:
            self.__message_type = 'feed_insertion'
            return

    @property
    def message_type(self):
        return self.__message_type

    @message_type.setter
    def message_type(self, message_type):
        pass

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        pass

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        pass

    @property
    def child_id(self):
        return self.__child_id

    @child_id.setter
    def child_id(self, child_id):
        pass

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, volume):
        pass

    @property
    def breast(self):
        return self.__breast

    @breast.setter
    def breast(self, breast):
        pass
