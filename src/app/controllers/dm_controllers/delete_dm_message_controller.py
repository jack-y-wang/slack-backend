from app.controllers import *
from flask import request
from app.dao import dms_dao

class DeleteDmMessageController(Controller):
    def get_name(self):
        return "delete-dm-message"
        
    def get_path(self):
        return "/dm-messages/<int:dm_id>/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        dm = dms_dao.delete_dm_message_by_id(dm_id, user.id)
        return dm.serialize()
        