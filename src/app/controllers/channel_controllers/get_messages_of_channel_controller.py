from app.controllers import *
from flask import request
from app.dao import channels_dao

class GetMessagesOfChannelController(Controller):
    def get_name(self):
        return "get-channel-messages"

    def get_path(self):
        return "/channels/<int:channel_id>/messages/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, channel_id):
        messages = channels_dao.get_messages_of_channel(channel_id)
        return [msg.serialize_content() for msg in messages]
        