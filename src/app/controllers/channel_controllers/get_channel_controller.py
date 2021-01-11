from app.controllers import *
from flask import request
from app.dao import channels_dao

class GetChannelController(Controller):
    def get_path(self):
        return "/channels/<int:channel_id>/"
    
    def get_methods(self):
        return ["GET"]
    
    @authorize_user
    def content(self, channel_id, **kwargs):
        user = kwargs.get("user")
        channel = channels_dao.get_channel_by_id(channel_id)
        if not user in channel.users:
            raise Excepation("User not in channel")
        return channel.serialize()
