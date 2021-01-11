from app.controllers import *
from flask import request
from app.dao import dms_dao

class UpdateDmMessageController(Controller):
    def get_name(self):
        return "update-dm-message"

    def get_path(self):
        return "/dm-messages/<int:message_id>/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, message_id, **kwargs):
        user = kwargs.get("user")
        data = request.get_json()
        content = data.get("content")

        dm = dms_dao.update_dm_message(message_id, user.id, content)
        return dm.serialize()
        