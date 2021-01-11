from app.controllers import *
from flask import request
from app.dao import dms_dao

class DeleteDmGroupController(Controller):
    def get_name(self):
        return "delete-dm-group"

    def get_path(self):
        return "/dms/<int:dm_group_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        dm_group = dms_dao.get_dm_group_by_id(dm_group_id)
        if user not in dm_group.users:
            raise Exception("User not in DM Group")
        dm_group = dms_dao.delete_dm_group_by_id(dm_id)
        return dm_group.serialize()
        