from app.controllers import *
from flask import request
from app.dao import users_dao

class UpdateProfilePicController(Controller):
    def get_path(self):
        return "/users/<user_id>/profile-img/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self):
        data = request.get_json()
        image = data.get("image")
        user_id = int(request.view_args["user_id"])

        user = users_dao.update_profile_image(user_id, image)
        return user.serialize()
