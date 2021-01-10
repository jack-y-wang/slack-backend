from app.controllers import *
from flask import request
from app.dao import users_dao

class DeleteUserController(Controller):
    def get_name(self):
        return "delete-user"

    def get_path(self):
        return "/user/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        user = users_dao.delete_user_by_id(user_id)
        return user.serialize()
