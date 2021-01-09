from app.controllers import *
from flask import request
from app.dao import dms_dao

class UpdateDmMessageController(Controller):
    def get_path(self):
        return "/dm-messages/<message_id>/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self):
        data = request.get_json()
        user_id = data.get("user_id")
        content = data.get("content")
        message_id = int(request.view_args["message_id"])

        dm = dms_dao.update_dm_message(message_id, user_id, content)
        return dm.serialize()
        