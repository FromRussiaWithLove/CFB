from db_handler_selector import DbHandlerSelector


class Response:

    def __init__(self, message='', chat='broadcast'):
        self.__chats = self.__chats_setup(chat)
        self.message = message

    def __chats_setup(self, chat):
        if chat != 'broadcast':
            return [chat]
        db_handler = DbHandlerSelector.get_db_handler()
        return db_handler.get_all_chats()

    @property
    def chats(self):
        return self.__chats

    @chats.setter
    def chats(self, chat):
        self.__chats = self.__chats_setup(chat)
