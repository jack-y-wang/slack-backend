from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUserImagesController(Controller):
    def get_path(self):
        return "/user/images/"
    
    def get_methods(self):
        return ["GET"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        images = users_dao.get_images_of_user(user.id)
        return [i.serialize() for i in images]
