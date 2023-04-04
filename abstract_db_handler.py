from abc import ABC, abstractmethod


class DbBaseModel(ABC):
    @classmethod
    @abstractmethod
    def init_db(cls):
        pass

    @classmethod
    @abstractmethod
    def connect_db(cls):
        pass

    @classmethod
    @abstractmethod
    def check_user(cls, user_id):
        pass

    @classmethod
    @abstractmethod
    def add_user(cls, user_id):
        pass

    @classmethod
    @abstractmethod
    def add_chat(cls, chat_id):
        pass

    @classmethod
    @abstractmethod
    def add_feeding(cls, feeding_date: int, message: list) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_all_chats(cls, ):
        pass

    @classmethod
    @abstractmethod
    def get_feedings(cls, message: list, n: int) -> str:
        pass

    @classmethod
    @abstractmethod
    def request_to_db(cls, request):
        pass

    @classmethod
    @abstractmethod
    def get_child_from_pseudo(cls, pseudo):
        pass
