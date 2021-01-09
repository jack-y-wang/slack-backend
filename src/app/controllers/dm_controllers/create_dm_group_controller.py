from app.controllers import *
from flask import request
from app.dao import dms_dao

class CreateDMGroupController(Controller):
    def get_path(self):
        return "/workspaces/<workspace_id>/dms/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self):
        data = request.get_json()
        users = data.get("users")
        workspace_id = int(request.view_args["workspace_id"])

        dm_group = dms_dao.create_dm_group(workspace_id, users)
        return dm_group.serialize()
        