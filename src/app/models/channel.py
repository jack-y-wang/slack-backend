from app import db
from app.models.association_tables import *

from app.models.workspace import Workspace


class Channel(db.Model):
    __tablename__ = "channel"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    public = db.Column(db.Boolean, nullable=False)
    workspace_id = db.Column(db.Integer, db.ForeignKey("workspace.id"), nullable=False)
    users = db.relationship(
        "User",
        secondary=association_table_userchannel,
        back_populates='channels'
    )
    messages = db.relationship("Message", cascade='delete')
    images = db.relationship("MessageImage", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.public = kwargs.get("public")
        self.workspace_id = kwargs.get("workspace_id")
    
    def serialize(self):
        workspace = Workspace.query.filter_by(id=self.workspace_id).first()
        if workspace is None:
            return None
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "workspace": workspace.serialize_name(),
            "users": [u.serialize_name() for u in self.users],
            "messages": [m.serialize_content() for m in self.messages] 
        }
    
    def serialize_name(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    def serialize_for_user(self):
        workspace = Workspace.query.filter_by(id=self.workspace_id).first()
        if workspace is None:
            return None
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "workspace": workspace.serialize_name(),
        }
    