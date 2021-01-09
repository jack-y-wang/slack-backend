from app.controllers import *
from flask import request
from app.dao import users_dao

class DeleteUserController(Controller):
    def get_name(self):
        return "delete-user"

    def get_path(self):
        return "/users/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        data = request.get_json()
        user_id = data.get("user_id")
        user = users_dao.delete_user_by_id(user_id)
        return user.serialize()
