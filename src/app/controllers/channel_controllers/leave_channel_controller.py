from app.controllers import *
from flask import request
from app.dao import channels_dao

class LeaveChannelController(Controller):
    def get_path(self):
        return "/channels/<int:channel_id>/leave/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, channel_id, **kwargs):
        user = kwargs.get("user")
        channel = channels_dao.get_channel_by_id(channel_id)
        if not user in channel.users:
            raise Excepation("User not in channel")
        channel = channels_dao.delete_user_from_channel(channel_id, user_id)
        return channel.serialize()
