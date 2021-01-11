from app.controllers import *
from flask import request
from app.dao import channels_dao

class AddUserToChannelController(Controller):
    def get_path(self):
        return "/channels/<int:channel_id>/users/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, channel_id, **kwargs):
        requester = kwargs.get("user")
        data = request.get_json()
        user_id = data.get("user_id")

        channel = channels_dao.get_channel_by_id(channel_id)
        if not channel.public:
            if channels_dao.is_user_in_channel(channel_id, requester.id):
                channel = channels_dao.add_user_to_channel(channel_id, user_id)
                return channel.serialize()
            else:
                raise Excepation("You are not in private channel")

        channel = channels_dao.add_user_to_channel(channel_id, user_id)
        return channel.serialize()