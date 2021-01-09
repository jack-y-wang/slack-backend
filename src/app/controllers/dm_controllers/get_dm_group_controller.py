from app.controllers import *
from flask import request
from app.dao import dms_dao

class GetDMGroupController(Controller):
    def get_name(self):
        return "get-dm-group" 

    def get_path(self):
        return "/dms/<dm_id>/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        dm_id = int(request.view_args["dm_id"])

        dm_group = dms_dao.get_dm_group_by_id(dm_id)
        return dm_group.serialize()
        