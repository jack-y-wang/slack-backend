from app.controllers import *
from flask import request
from app.dao import threads_dao

class CreateThreadController(Controller):
    def get_name(self):
        return "create-thread"

    def get_path(self):
        return "/messages/<int:message_id>/threads/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, message_id, **kwargs):
        user = kwargs.get("user")
        data = request.get_json()
        content = data.get("content")
        image = data.get("image")

        thread = threads_dao.create_thread(message_id, user.id, content, image)
        return thread.serialize()
        