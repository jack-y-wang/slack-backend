from app.controllers import *
from flask import request
from app.dao import dms_dao

class DeleteDmGroupController(Controller):
    def get_name(self):
        return "delete-dm-group"

    def get_path(self):
        return "/dms/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        data = request.get_json()
        dm_id = data.get("dm_group_id")
        dm_group = dms_dao.delete_dm_group_by_id(dm_id)
        return dm_group.serialize()
        