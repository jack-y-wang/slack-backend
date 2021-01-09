from app.controllers import *
from flask import request
from app.dao import dms_dao

class DeleteDmMessageController(Controller):
    def get_name(self):
        return "delete-dm-message"
        
    def get_path(self):
        return "/dm-messages/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        data = request.get_json()
        dm_id = data.get("dm_id")
        dm = dms_dao.delete_dm_message_by_id(dm_id)
        return dm.serialize()
        