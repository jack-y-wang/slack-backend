from app.controllers import *
from flask import request
from app.dao import threads_dao

class RemoveThreadController(Controller):
    def get_name(self):
        return "remove-thread"

    def get_path(self):
        return "/threads/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        data = request.get_json()
        thread_id = data.get("thread_id")
        thread = threads_dao.delete_thread_by_id(thread_id)
        return thread.serialize()
        