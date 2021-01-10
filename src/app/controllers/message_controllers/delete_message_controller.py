from app.controllers import *
from flask import request
from app.dao import messages_dao

class DeleteMessageController(Controller):
    def get_name(self):
        return "delete-message"

    def get_path(self):
        return "/messages/<int:message_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    @authorize_user
    def content(self, message_id, **kwargs):
        user = kwargs.get("user")
        message = messages_dao.delete_message_by_id(message_id, user.id)
        return message.serialize()
        