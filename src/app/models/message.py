from app import db
from app.models.association_tables import *

from app.models.asset import Asset
from app.models.channel import Channel


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("message_image.id"), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"))
    threads = db.relationship("Thread", back_populates='message', cascade='delete')
    users_following = db.relationship(
        "User", 
        secondary=association_table_userthread, 
        back_populates='threads')
    updated = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.sender_id = kwargs.get("sender_id")
        self.content = kwargs.get("content")
        self.timestamp = kwargs.get("timestamp")
        self.channel_id = kwargs.get("channel_id")
        self.updated = False
    
    def serialize(self):
        channel = Channel.query.filter_by(id=self.channel_id).first()
        if channel is None:
            return None

        image = Asset.query.filter_by(id=self.image_id).first()
        if image is None:
            image_serialized = None
        else:
            image_serialized = image.serialize_for_message()

        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "image": image_serialized,
            "timestamp": str(self.timestamp),
            "channel": channel.serialize(),
            "threads": [t.serialize_content() for t in self.threads],
            "users_following": [u.serialize_name() for u in self.users_following],
            "updated": self.updated
        }
    
    def serialize_content(self):
        image = Asset.query.filter_by(id=self.image_id).first()
        if image is None:
            image_serialized = None
        else:
            image_serialized = image.serialize_for_message()
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "image": image_serialized,
            "content": self.content,
            "timestamp": str(self.timestamp),
            "updated": self.updated
        }
