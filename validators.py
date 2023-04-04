import hashlib

import settings
from db_handler_selector import DbHandlerSelector


class UserValidator:

    @classmethod
    def __validate_password(cls, password_to_check):
        hssh = hashlib.pbkdf2_hmac(
            'sha256',
            password_to_check.encode('utf-8'),
            settings.salt,
            100000
        )

        if hssh == settings.mainPasswordHash:
            return True
        return False

    @classmethod
    def validate_user(cls, message, user_id):
        db_handler = DbHandlerSelector.get_db_handler()
        if db_handler.check_user(user_id):
            return True
        if cls.__validate_password(message):
            db_handler.add_user(user_id)
            return True
        return False
