from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class CreateWorkspaceController(Controller):
    def get_name(self):
        return "create-workspace"

    def get_path(self):
        return "/workspaces/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        data = request.get_json()
        name = data.get("name")
        url = data.get("url")

        workspace = workspaces_dao.create_workspace(name, url)
        workspace = workspaces_dao.add_user_to_workspace(user.id, workspace.id)
        return workspace.serialize()
