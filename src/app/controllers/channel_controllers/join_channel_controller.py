from app.controllers import *
from flask import request
from app.dao import channels_dao

class JoinChannelController(Controller):
    def get_path(self):
        return "/channels/<int:channel_id>/join/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, channel_id, **kwargs):
        user = kwargs.get("user")

        channel = channels_dao.get_channel_by_id(channel_id)
        if user in channel.users:
            raise Exception("Already in channel")
        if not channel.public:
            raise Exception("Private Channel - must be added by someone in channel")

        channel = channels_dao.add_user_to_channel(channel_id, user_id)
        return channel.serialize()