from app import db
from app.models.association_tables import *

class Workspace(db.Model):
    __tablename__ = "workspace"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    channels = db.relationship("Channel", cascade="delete")
    users = db.relationship(
        "User", 
        secondary=association_table_userworksp,
        back_populates="workspaces"
    )
    images = db.relationship("MessageImage", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "users": [u.serialize_name() for u in self.users],
            "channels": self.serialize_public_channels()
        }
    
    def serialize_name(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }
    
    def serialize_public_channels(self):
        return [c.serialize_name() for c in self.channels if c.public]
