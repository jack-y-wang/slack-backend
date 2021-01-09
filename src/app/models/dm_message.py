from app import db
from app.models.association_tables import *

from app.models.user import User
from app.models.dm_group import DM_group

class DM_message(db.Model):
    __tablename__ = "dm_message"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)
    dm_group_id = db.Column(db.Integer, db.ForeignKey("dm_group.id"), nullable=False)
    updated = db.Column(db.Boolean, nullable = False)

    def __init__(self, **kwargs):
        self.sender_id = kwargs.get("sender_id")
        self.content = kwargs.get("content")
        self.timestamp = kwargs.get("timestamp")
        self.dm_group_id = kwargs.get("dm_group_id")
        self.udpated = False
    
    def serialize(self):
        sender = User.query.filter_by(id=self.sender_id).first()
        if sender is None:
            return None
        dm_group = DM_group.query.filter_by(id=self.dm_group_id).first()
        if dm_group is None:
            return None
        return {
            "id": self.id,
            "sender": sender.serialize_name(),
            "content": self.content,
            "timestamep": str(self.timestamp),
            "updated": self.updated,
            "dm_group": dm_group.serialize_dm_group()
        }
    
    def serialize_dm(self):
        sender = User.query.filter_by(id=self.sender_id).first()
        if sender is None:
            return None
        return {
            "id": self.id,
            "sender": sender.serialize_name(),
            "content": self.content,
            "timestamep": str(self.timestamp),
            "updated": self.updated
        }
