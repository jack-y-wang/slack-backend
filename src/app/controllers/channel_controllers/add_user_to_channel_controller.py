from app.controllers import *
from flask import request
from app.dao import channels_dao

class AddUserToChannelController(Controller):
    def get_path(self):
        return "/channels/<int:channel_id>/users/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self, channel_id):
        data = request.get_json()
        user_id = data.get("user_id")
        channel = channels_dao.add_user_to_channel(channel_id, user_id)
        return channel.serialize()