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
    
    def content(self, channel_id):
        data = request.get_json()
        user_id = data.get("user_id")
        content = data.get("content")
        image = data.get("image")

        message = messages_dao.create_message(channel_id, user_id, content, image)
        return message.serialize()