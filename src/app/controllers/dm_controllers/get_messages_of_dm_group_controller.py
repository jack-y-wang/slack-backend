from app.controllers import *
from flask import request
from app.dao import dms_dao

class GetMessagesOfDMGroupController(Controller):
    def get_path(self):
        return "/dms/<dm_id>/messages/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        dm_id = int(request.view_args["dm_id"])
        messages = dms_dao.get_messages_of_dm_group(dm_id)
        return [m.serialize_dm() for m in messages]
        