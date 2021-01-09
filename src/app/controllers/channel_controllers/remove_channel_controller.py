from app.controllers import *
from flask import request
from app.dao import channels_dao

class RemoveChannelController(Controller):
    def get_path(self):
        return "/channels/<channel_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        channel_id = int(request.view_args["channel_id"])
        channel = channels_dao.delete_channel(channel_id)
        return channel.serialize()
        