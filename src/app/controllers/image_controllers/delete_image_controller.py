from app.controllers import *
from flask import request
from app.dao import images_dao

class DeleteImageController(Controller):
    def get_path(self):
        return "/images/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        data = request.get_json()
        image_id = data.get("image_id")
        return images_dao.delete_image_by_id(image_id).serialize()
