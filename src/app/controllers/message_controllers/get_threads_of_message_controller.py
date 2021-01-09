from app.controllers import *
from flask import request
from app.dao import messages_dao

class GetThreadsOfMessageController(Controller):
    def get_path(self):
        return "/messages/<int:message_id>/threads/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, message_id):
        threads = messages_dao.get_threads_of_message(message_id)
        return [t.serialize_content() for t in threads]
        