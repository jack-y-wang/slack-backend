from app import db
from app.models.association_tables import *

from app.models.asset import Asset


class Thread(db.Model):
    __tablename__ = "thread"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey("message.id"), nullable=False)
    message = db.relationship("Message", back_populates="threads")
    image_id = db.Column(db.Integer, db.ForeignKey("message_image.id"), nullable=True)
    updated = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.sender_id = kwargs.get("sender_id")
        self.content = kwargs.get("content")
        self.timestamp = kwargs.get("timestamp")
        self.message_id = kwargs.get("message_id")
        self.updated = False
    
    def serialize(self):
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
            "message": self.message.serialize_content(),
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
            "content": self.content,
            "image": image_serialized,
            "timestamp": str(self.timestamp),
            "updated": self.updated
        }
