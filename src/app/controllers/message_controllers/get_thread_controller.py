from app.controllers import *
from flask import request
from app.dao import threads_dao

class GetThreadController(Controller):
    def get_path(self):
        return "/threads/<thread_id>"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        thread_id = int(request.view_args["thread_id"])
        thread = threads_dao.get_thread_by_id(thread_id)
        return thread.serialize()
        