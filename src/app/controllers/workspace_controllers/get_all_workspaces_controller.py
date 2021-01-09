from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class GetAllWorkspaceController(Controller):
    def get_path(self):
        return "/workspaces/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        workspaces = workspaces_dao.get_workspaces()
        return [w.serialize() for w in workspaces]
        