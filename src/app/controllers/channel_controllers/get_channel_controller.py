from app.controllers import *
from flask import request
from app.dao import channels_dao

class GetChannelController(Controller):
    def get_path(self):
        return "/channels/<int:channel_id>/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, channel_id):
        return channels_dao.get_channel_by_id(channel_id)
