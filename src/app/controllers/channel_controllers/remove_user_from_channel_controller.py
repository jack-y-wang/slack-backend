from app.controllers import *
from flask import request
from app.dao import channels_dao

class RemoveUserFromChannelController(Controller):
    def get_path(self):
        return "/channels/<channel_id>/users/<user_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        channel_id = int(request.view_args["channel_id"])
        user_id = int(request.view_args["user_id"])
        channel = channels_dao.delete_user_from_channel(channel_id, user_id)
        return channel.serialize()
