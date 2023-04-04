import datetime

# Токен бота
token = ''

# Смещение часового пояса
delta = datetime.timedelta(hours=3, minutes=0)

# Путь к базе данных
database = {'user': '',
            'password': '',
            'host': '',
            'port': '',
            'dbname': '',
            'postgresdb': '',
            'type' : '',
            }

# Записей в сообщении по умолчанию
feedingsPerMessageDefault = 9

# Соль для хэширования пароля
salt = b''

# Хэш пароля
mainPasswordHash = b''

# Предопределенные значения базы данных
childsDefault = {'Ребенок1': ('ребенок1', 'реб1', 'ребетенок1', '1'),
                 }