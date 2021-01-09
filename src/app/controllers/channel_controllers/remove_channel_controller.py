from app.controllers import *
from flask import request
from app.dao import channels_dao

class RemoveChannelController(Controller):
    def get_name(self):
        return "remove-channel"

    def get_path(self):
        return "/channels/remove/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        data = request.get_json()
        channel_id = data.get("channel_id")
        channel = channels_dao.delete_channel(channel_id)
        return channel.serialize()
        