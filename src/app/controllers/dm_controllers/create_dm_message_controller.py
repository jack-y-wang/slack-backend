from app.controllers import *
from flask import request
from app.dao import dms_dao

class CreateDmMessageController(Controller):
    def get_name(self):
        return "create-dm-message"
        
    def get_path(self):
        return "/dms/<int:dm_id>/messages/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self, dm_id):
        data = request.get_json()
        user_id = data.get("user_id")
        content = data.get("content")

        dm = dms_dao.create_dm_message(dm_id, user_id, content)
        return dm.serialize()
        