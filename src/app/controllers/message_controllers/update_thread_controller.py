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
    
    def content(self, thread_id):
        data = request.get_json()
        user_id = data.get("user_id")
        content = data.get("content")

        thread = threads_dao.update_thread_by_id(thread_id, user_id, content)
        return thread.serialize()
        