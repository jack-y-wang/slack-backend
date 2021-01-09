from app.controllers import *
from flask import request
from app.dao import threads_dao

class RemoveThreadController(Controller):
    def get_path(self):
        return "/threads/<thread_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        thread_id = int(request.view_args["thread_id"])
        thread = threads_dao.delete_thread_by_id(thread_id)
        return thread.serialize()
        