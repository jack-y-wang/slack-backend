from app.controllers import *
from flask import request
from app.dao import dms_dao

class DeleteDmMessageController(Controller):
    def get_path(self):
        return "/dm-messages/<message_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        dm_id = int(request.view_args["dm_id"])
        dm = dms_dao.delete_dm_message_by_id(dm_id)
        return dm.serialize()
        