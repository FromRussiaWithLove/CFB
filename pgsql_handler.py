import psycopg2

import settings
from abstract_db_handler import DbBaseModel
from tabulators import DefaultTabulator


class PostgreHandler(DbBaseModel):
    @classmethod
    def init_db(cls):
        # Пробуем подключиться к серверу
        try:
            connection = psycopg2.connect(user=settings.database['user'],
                                          password=settings.database['password'],
                                          host=settings.database['host'],
                                          port=settings.database['port'],
                                          dbname=settings.database['postgresdb'])
            cursor = connection.cursor()
        except:
            return
        # По умолчанию первичное заполнение базы не нужно
        first_filling_needed = False
        try:
            # Пробуем создать базу, если база была создана, требуется первичное заполнение
            connection.autocommit = True
            cursor.execute('CREATE DATABASE ' + settings.database['dbname'])
            first_filling_needed = True
        except Exception as e:
            pass
        finally:
            cursor.close()
            connection.close()

        # Создаем таблицы
        try:
            connection = cls.connect_db()
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS childs (
                           Id SERIAL PRIMARY KEY,
                           name TEXT CONSTRAINT name_unique UNIQUE) 
                           ''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS feeds (
                            Id SERIAL PRIMARY KEY,
                            child INTEGER,
                            datetime INTEGER,
                            content	TEXT,
                            FOREIGN KEY (child) REFERENCES childs(Id) ON DELETE RESTRICT)
                           ''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS pseudonyms (
                            Id SERIAL PRIMARY KEY,
                            child INTEGER,
                            pseudonym TEXT CONSTRAINT pseudonym_unique UNIQUE,
                            FOREIGN KEY(child) REFERENCES childs(Id) ON DELETE RESTRICT)
                           ''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                            Id SERIAL PRIMARY KEY,
                            telegram_id INTEGER CONSTRAINT telegram_id UNIQUE)
                            ''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS chats(
                            Id SERIAL PRIMARY KEY,
                            chat_id INTEGER CONSTRAINT chat_id_unique UNIQUE)
                            ''')

            connection.commit()

            # Заполняем базу значениями по умолчанию
            if first_filling_needed:
                child_id = 1
                for name, pseudonyms in settings.childsDefault.items():
                    cursor.execute('''INSERT INTO childs (name) VALUES
                            (%s)''', (name,))
                    connection.commit()
                    for pseudonym in pseudonyms:
                        cursor.execute('''INSERT INTO pseudonyms (child, pseudonym) VALUES
                            (%s, %s)''', (child_id, pseudonym))
                        connection.commit()
                    child_id += 1
        except Exception as e:
            pass
        finally:
            if connection:
                cursor.close()
                connection.close()

    @classmethod
    def connect_db(cls):
        return psycopg2.connect(user=settings.database['user'],
                                password=settings.database['password'],
                                host=settings.database['host'],
                                port=settings.database['port'],
                                dbname=settings.database['dbname'])

    @classmethod
    def check_user(cls, user_id):
        try:
            connection = cls.connect_db()
            cursor = connection.cursor()
            cursor.execute('SELECT Id FROM users WHERE telegram_id = %s', (user_id,))
            result = not (cursor.fetchall() == [])
        except Exception as e:
            result = False
        finally:
            if connection:
                cursor.close()
                connection.close()
            return result

    @classmethod
    def add_user(cls, user_id):
        try:
            connection = cls.connect_db()
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO users (telegram_id) VALUES
                    (%s)''', (user_id,))
            connection.commit()
        except Exception as e:
            pass
        finally:
            if connection:
                cursor.close()
                connection.close()

    @classmethod
    def add_chat(cls, chat_id):
        try:
            connection = cls.connect_db()
            cursor = connection.cursor()
            cursor.execute('''SELECT id FROM chats WHERE chat_id=%s''', (chat_id,))
            if not cursor.fetchall():
                cursor.execute('''INSERT INTO chats (chat_id) VALUES (%s)''', (chat_id,))
                connection.commit()
        except Exception as e:
            pass
        finally:
            if connection:
                cursor.close()
                connection.close()

    @classmethod
    def add_feeding(cls, timestamp: int, child_id: int, content: str) -> str:

        try:
            connection = cls.connect_db()
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO feeds(child, datetime, content)
                            VALUES(%s, %s, %s)''',
                           (child_id,
                            timestamp,
                            content,
                            ))
            connection.commit()
            response = cls.get_feedings(child_id, settings.feedingsPerMessageDefault)
        except Exception as e:
            response = e
        finally:
            if connection:
                cursor.close()
                connection.close()
            return response

    @classmethod
    def get_all_chats(cls):
        try:
            connection = cls.connect_db()
            cursor = connection.cursor()
            cursor.execute('SELECT chat_id FROM chats')
            result = [x[0] for x in cursor.fetchall()]
        except Exception as e:
            result = []
        finally:
            if connection:
                cursor.close()
                connection.close()
            return result

    @classmethod
    def get_feedings(cls, child_id: int, n: int) -> str:
        response = 'Нет данных'
        try:
            connection = cls.connect_db()
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM childs WHERE id = %s', (child_id,))
            child_name = cursor.fetchone()[0]
            query = """SELECT * from (SELECT
                    (SELECT name from childs WHERE id=feeds.child) as child_name,
                    datetime,
                    content
                    FROM feeds
                    WHERE child = %s
                    ORDER BY datetime DESC limit %s) as tt_data
                    ORDER BY datetime"""
            cursor.execute(query, (child_id, n))
            rows = cursor.fetchall()
            if rows:
                response = DefaultTabulator.get_pretty_table(rows, child_name)
        except Exception as e:
            response = e
        finally:
            if connection:
                cursor.close()
                connection.close()
            return response

    @classmethod
    def request_to_db(cls, request):
        request = request.lower().replace('sql ', '')
        try:
            connection = cls.connect_db()
            cursor = connection.cursor()
            cursor.execute(request)
            if request.startswith('select'):
                data = cursor.fetchall()
                response = str(data)
            else:
                response = 'done'
        except Exception as e:
            response = e
        finally:
            if connection:
                connection.commit()
                cursor.close()
                connection.close()
            return response

    @classmethod
    def get_child_from_pseudo(cls, pseudo):
        try:
            connection = cls.connect_db()
            cursor = connection.cursor()
            cursor.execute('SELECT child from pseudonyms WHERE pseudonym = %s', (pseudo,))
            result = cursor.fetchone()[0]
        except Exception as e:
            result = None
        finally:
            if connection:
                cursor.close()
                connection.close()
            return result
