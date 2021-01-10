from app.controllers import *
from flask import request
from app.dao import threads_dao

class UpdateThreadController(Controller):
    def get_name(self):
        return "update-thread"

    def get_path(self):
        return "/threads/<int:thread_id>/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, thread_id, **kwargs):
        user = kwargs.get("user")
        data = request.get_json()
        content = data.get("content")

        thread = threads_dao.update_thread_by_id(thread_id, user.id, content)
        return thread.serialize()
        