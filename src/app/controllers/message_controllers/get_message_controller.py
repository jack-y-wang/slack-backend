from app.controllers import *
from flask import request
from app.dao import messages_dao

class GetMessageController(Controller):
    def get_name(self):
        return "get-message"

    def get_path(self):
        return "/messages/<int:message_id>/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, message_id):
        message = messages_dao.get_message_by_id(message_id)
        return message.serialize()
        