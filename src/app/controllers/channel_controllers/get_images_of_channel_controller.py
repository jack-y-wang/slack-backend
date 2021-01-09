from app.controllers import *
from flask import request
from app.dao import channels_dao

class GetImagesOfChannelController(Controller):
    def get_path(self):
        return "/channels/<int:channel_id>/images/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, channel_id):
        images = channels_dao.get_images_of_channel(channel_id)
        return [image.serialize() for image in images]
