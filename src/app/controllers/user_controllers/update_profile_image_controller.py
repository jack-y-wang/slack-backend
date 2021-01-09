from app.controllers import *
from flask import request
from app.dao import users_dao

class UpdateProfilePicController(Controller):
    def get_path(self):
        return "/users/update-profile-image/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self):
        data = request.get_json()
        image = data.get("image")
        user_id = data.get("user_id")

        user = users_dao.update_profile_image(user_id, image)
        return user.serialize()
