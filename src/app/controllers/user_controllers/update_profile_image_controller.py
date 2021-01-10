from app.controllers import *
from flask import request
from app.dao import users_dao

class UpdateProfilePicController(Controller):
    def get_path(self):
        return "/update-profile/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        data = request.get_json()
        image = data.get("image")

        user = users_dao.update_profile_image(user.id, image)
        return user.serialize()
