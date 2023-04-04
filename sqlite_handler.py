import sqlite3
import re

import datetime_methods
import settings
from abstract_db_handler import DbBaseModel


class SQLiteHandler(DbBaseModel):
    @classmethod
    def init_db(cls):
        pass

    @classmethod
    def connect_db(cls):
        pass

    @classmethod
    def check_user(cls, user_id):
        pass

    @classmethod
    def add_user(cls, user_id):
        pass

    @classmethod
    def add_chat(cls, chat_id):
        pass

    @classmethod
    def add_feeding(cls, feeding_date: int, message: list) -> str:
        pass

    @classmethod
    def get_all_chats(cls):
        pass

    @classmethod
    def get_feedings(cls, message: list, n: int) -> str:
        pass

    @classmethod
    def request_to_db(cls, request):
        pass
