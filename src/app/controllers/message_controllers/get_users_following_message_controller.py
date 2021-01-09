from app.controllers import *
from flask import request
from app.dao import messages_dao

class GetUsersFollowingMessageController(Controller):
    def get_path(self):
        return "/messages/<int:message_id>/users/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, message_id):
        users = messages_dao.get_users_following_message(message_id)
        return [u.serialize() for u in users]