from app.controllers import *
from flask import request
from app.dao import messages_dao

class CreateMessageController(Controller):
    def get_name(self):
        return "create-message"
        
    def get_path(self):
        return "/channels/<int:channel_id>/messages/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, channel_id, **kwargs):
        user = kwargs.get("user")
        data = request.get_json()
        content = data.get("content")
        image = data.get("image")

        message = messages_dao.create_message(channel_id, user.id, content, image)
        return message.serialize()