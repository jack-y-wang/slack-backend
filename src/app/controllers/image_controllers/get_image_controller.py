from app.controllers import *
from flask import request
from app.dao import images_dao

class GetImageController(Controller):
    def get_path(self):
        return "/images/<int:image_id>/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, image_id):
        return images_dao.get_image_by_id(image_id).serialize()
