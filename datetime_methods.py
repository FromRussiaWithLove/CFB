import datetime
import time

import settings


def timestamp_from_time(message_timestamp, time_string):
    message_date = date_time_from_timestamp(message_timestamp)[0]
    message_date = message_date.split('.')
    time_string = f'{message_date[2]}-{message_date[1]}-{message_date[0]} {time_string[:-3]}:{time_string[-2:]}'
    return time.mktime((datetime.datetime.strptime(time_string,
                                                   "%Y-%m-%d %H:%M") - settings.delta).timetuple())


def date_time_from_timestamp(timestamp):
    feed_date_time = str(datetime.datetime.utcfromtimestamp(timestamp) + settings.delta)
    feed_date, feed_time = feed_date_time.split()
    feed_date_list = feed_date.split('-')
    if len(feed_date_list) == 3:
        feed_date = f'{feed_date_list[2]}.{feed_date_list[1]}.{feed_date_list[0]}'
    return feed_date, feed_time
