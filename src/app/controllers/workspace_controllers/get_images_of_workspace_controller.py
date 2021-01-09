from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class GetImagesOfWorkspaceController(Controller):
    def get_path(self):
        return "/workspaces/<int:workspace_id>/images/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, workspace_id):
        images = workspaces_dao.get_images_of_workspace(workspace_id)
        return [img.serialize() for img in images]
        