from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class CreateWorkspaceController(Controller):
    def get_path(self):
        return "/workspaces/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self):
        data = request.get_json()
        name = data.get("name")
        url = data.get("url")

        workspace = workspaces_dao.create_workspace(name, url)
        return workspace.serialize()
