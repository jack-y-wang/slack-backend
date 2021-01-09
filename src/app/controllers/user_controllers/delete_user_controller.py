from app.controllers import *
from flask import request
from app.dao import users_dao

class DeleteUserController(Controller):
    def get_path(self):
        return "/users/<user_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        user_id = int(request.view_args["user_id"])

        user = users_dao.delete_user_by_id(user_id)
        return user.serialize()
