from app.controllers import *
from flask import request
from app.dao import threads_dao

class RemoveThreadController(Controller):
    def get_name(self):
        return "remove-thread"

    def get_path(self):
        return "/threads/<int:thread_id>/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    @authorize_user
    def content(self, thread_id, **kwargs):
        user = kwargs.get("user")
        thread = threads_dao.delete_thread_by_id(thread_id, user.id)
        return thread.serialize()
        