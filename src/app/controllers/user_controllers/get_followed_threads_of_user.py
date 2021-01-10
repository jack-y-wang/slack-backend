from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUsersFollowedThreadsController(Controller):
    def get_path(self):
        return "/user/threads/"
    
    def get_methods(self):
        return ["GET"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        threads = users_dao.get_threads_of_user(user.id)
        return [m.serialize_content() for m in threads]
