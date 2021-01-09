from app.controllers import *
from flask import request
from app.dao import dms_dao

class GetDmMessageController(Controller):
    def get_name(self):
        return "get-dm-message"

    def get_path(self):
        return "/dm-messages/<int:message_id>/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, message_id):
        dm = dms_dao.get_dm_message_by_id(message_id)
        return dm.serialize()
        