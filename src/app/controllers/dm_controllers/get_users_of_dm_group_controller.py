from app.controllers import *
from flask import request
from app.dao import dms_dao

class GetUsersOfDMGroup(Controller):
    def get_path(self):
        return "/dms/<int:dm_id>/users/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, dm_id):
        users = dms_dao.get_users_of_dm_group(dm_id)
        return [u.serialize_name() for u in users]
        