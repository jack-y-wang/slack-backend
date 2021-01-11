from app.controllers import *
from flask import request
from app.dao import dms_dao

class GetMessagesOfDMGroupController(Controller):
    def get_path(self):
        return "/dms/<int:dm_id>/messages/"
    
    def get_methods(self):
        return ["GET"]
    
    @authorize_user
    def content(self, dm_id, **kwargs):
        user = kwargs.get("user")
        dm_group = dms_dao.get_dm_group_by_id(dm_id)
        if user not in dm_group.users:
            raise Exception("User not in DM Group")
        messages = dms_dao.get_messages_of_dm_group(dm_id)
        return [m.serialize_dm() for m in messages]
        