from app.controllers import *
from flask import request
from app.dao import channels_dao

class RemoveUserFromChannelController(Controller):
    def get_path(self):
        return "/channels/<int:channel_id>/users/<int:user_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self, channel_id, user_id):
        channel = channels_dao.delete_user_from_channel(channel_id, user_id)
        return channel.serialize()
