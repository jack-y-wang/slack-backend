from app.controllers import *
from flask import request
from app.dao import messages_dao

class UpdateMessageController(Controller):
    def get_name(self):
        return "update-message"
        
    def get_path(self):
        return "/messages/<int:message_id>/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, message_id, **kwargs):
        user = kwargs.get("user")
        data = request.get_json()
        content = data.get("content")

        message = messages_dao.update_message(message_id, user.id, content)
        return message.serialize()