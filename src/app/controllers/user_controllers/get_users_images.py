from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUserImagesController(Controller):
    def get_path(self):
        return "/users/<user_id>/images/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        user_id = int(request.view_args["user_id"])

        images = users_dao.get_images_of_user(user_id)
        return [i.serialize() for i in images]
