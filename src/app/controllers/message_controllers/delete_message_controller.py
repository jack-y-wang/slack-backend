from app.controllers import *
from flask import request
from app.dao import messages_dao

class DeleteMessageController(Controller):
    def get_name(self):
        return "delete-message"

    def get_path(self):
        return "/messages/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        data = request.get_json()
        message_id = data.get("message_id")
        message = messages_dao.delete_message_by_id(message_id)
        return message.serialize()
        