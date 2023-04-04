from db_handler_selector import DbHandlerSelector
from response_models import Response
from message_parsers import MessageParser
import settings


class MessageHandler:
    @staticmethod
    def handle_message(message: object) -> str:
        db_handler = DbHandlerSelector.get_db_handler()
        db_handler.add_chat(message.chat.id)
        response = Response(chat=message.chat.id)
        parsed_message = MessageParser(message)
        match parsed_message.message_type:
            case 'sql_request':
                response.message = db_handler.request_to_db(parsed_message.content)
            case 'feed_request':
                response.message = db_handler.get_feedings(parsed_message.child_id,
                                                           settings.feedingsPerMessageDefault)
            case 'feed_insertion':
                response.message = db_handler.add_feeding(parsed_message.timestamp,
                                                          parsed_message.child_id,
                                                          parsed_message.content)
                response.chats = 'broadcast'
            case _:
                response.message = 'Unknown request'
        return response
