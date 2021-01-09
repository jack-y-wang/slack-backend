from app.controllers import *
from flask import request
from app.dao import dms_dao

class GetDmMessageController(Controller):
    def get_path(self):
        return "/dm-messages/<message_id>/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        message_id = int(request.view_args["message_id"])

        dm = dms_dao.get_dm_message_by_id(message_id)
        return dm.serialize()
        