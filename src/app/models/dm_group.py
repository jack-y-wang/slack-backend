from app import db
from app.models.association_tables import *

from app.models.workspace import Workspace

class DM_group(db.Model):
    __tablename__ = "dm_group"

    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey("workspace.id"), nullable=False)
    users = db.relationship("User", secondary=association_table_userdm, back_populates="dms")
    messages = db.relationship("DM_message", cascade="delete")

    def __init__(self, **kwargs):
        self.workspace_id = kwargs.get("workspace_id")
    
    def serialize(self):
        workspace = Workspace.query.filter_by(id=self.workspace_id).first()
        if workspace is None:
            return None
        return {
            "id": self.id,
            "worskpace": workspace.serialize_name(),
            "users": [u.serialize_name() for u in self.users],
            "messages": [m.serialize_dm() for m in self.messages]
        }
    
    def serialize_dm_group(self):
        workspace = Workspace.query.filter_by(id=self.workspace_id).first()
        if workspace is None:
            return None
        return {
            "id": self.id,
            "worskpace": workspace.serialize_name(),
            "users": [u.serialize_name() for u in self.users],
        }
