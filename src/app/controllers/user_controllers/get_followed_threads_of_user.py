from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUsersFollowedThreadsController(Controller):
    def get_path(self):
        return "/users/<user_id>/threads/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        user_id = int(request.view_args["user_id"])
        threads = users_dao.get_threads_of_user(user_id)
        return [m.serialize_content() for m in threads]
