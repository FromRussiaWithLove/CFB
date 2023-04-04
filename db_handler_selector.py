import settings
from pgsql_handler import PostgreHandler
from sqlite_handler import SQLiteHandler


class DbHandlerSelector:

    @staticmethod
    def get_db_handler():

        match settings.database['type']:
            case 'pgsql':
                return PostgreHandler
            case 'sqlite':
                return SQLiteHandler
            case _:
                return None
