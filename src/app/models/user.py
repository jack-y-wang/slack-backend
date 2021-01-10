from app import db
from app.models.association_tables import *

from app.models.asset import Asset
from app.models.session import Session

import bcrypt

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)

    # User info
    name = db.Column(db.String, nullable="False")
    username = db.Column(db.String, nullable="False", unique=True)
    email = db.Column(db.String, nullable="False")
    password_digest = db.Column(db.String, nullable=False)

    # Session informaiton
    sessions = db.relationship("Session", back_populates="user", cascade="all, delete")
    
    profile_image_id = db.Column(db.Integer, db.ForeignKey("profile_image.id"), nullable=True)
    workspaces = db.relationship(
        "Workspace", 
        secondary=association_table_userworksp,
        back_populates="users"
    )
    channels = db.relationship(
        "Channel",
        secondary=association_table_userchannel,
        back_populates="users"
    )
    threads = db.relationship(
        "Message",
        secondary=association_table_userthread,
        back_populates="users_following"
    )
    dms = db.relationship(
        "DM_group",
        secondary=association_table_userdm,
        back_populates="users"
    )
    images = db.relationship("MessageImage", cascade="delete")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
        self.password_digest = bcrypt.hashpw(
            kwargs.get('password').encode('utf8'),
            bcrypt.gensalt(rounds=13)
        )
    
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)
    
    def serialize(self):
        if self.profile_image_id is None:
            profile_img = None
        else:
            profile_img = Asset.query.filter_by(id=self.profile_image_id).first()
            profile_img = profile_img.serialize()
            
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "profile_img": profile_img,
            "workspaces": [w.serialize_name() for w in self.workspaces]
        }
    
    def serialize_name(self):
        if self.profile_image_id is None:
            profile_img = None
        else:
            profile_img = Asset.query.filter_by(id=self.profile_image_id).first()
            profile_img = profile_img.serialize()

        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "profile_img": profile_img,
        }

    def serialize_channels(self):
        return [c.serialize_for_user() for c in self.channels]
