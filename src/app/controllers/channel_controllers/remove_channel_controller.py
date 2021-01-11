from app.controllers import *
from flask import request
from app.dao import channels_dao

class RemoveChannelController(Controller):
    def get_name(self):
        return "remove-channel"

    def get_path(self):
        return "/channels/<int:channel_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        channel = channels_dao.get_channel_by_id(channel_id)
        
        if not channel.public:
            if channels_dao.is_user_in_channel(channel_id, requester.id):
                channel = channels_dao.delete_channel(channel_id)
                return channel.serialize()
            else:
                raise Excepation("You are not in private channel")

        channel = channels_dao.delete_channel(channel_id)
        return channel.serialize()
        