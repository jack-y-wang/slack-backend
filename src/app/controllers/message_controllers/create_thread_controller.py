from app.controllers import *
from flask import request
from app.dao import threads_dao

class CreateThreadController(Controller):
    def get_name(self):
        return "create-thread"

    def get_path(self):
        return "/messages/<message_id>/threads/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self):
        data = request.get_json()
        user_id = data.get("user_id")
        content = data.get("content")
        image = data.get("image")
        message_id = int(request.view_args["message_id"])

        thread = threads_dao.create_thread(message_id, user_id, content, image)
        return thread.serialize()
        