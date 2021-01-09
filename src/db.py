from flask_sqlalchemy import SQLAlchemy

import base64
import boto3
import datetime
from io import BytesIO
from mimetypes import guess_extension, guess_type
import os
from PIL import Image
import random
import re
import string

db = SQLAlchemy()

EXTENSIONS = ["png", "gif", "jpg", "jpeg"]

BASE_DIR = os.getcwd()

S3_BUCKET = "slack-backend-images"
S3_BASE_URL = f"https://{S3_BUCKET}.s3-us-west-1.amazonaws.com"

association_table_userworksp = db.Table(
    "association_table_userworksp",
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('workspace_id', db.Integer, db.ForeignKey('workspace.id'))
)

association_table_userchannel = db.Table(
    "association_table_userchannel",
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'))
)

association_table_userthread = db.Table(
    "association_table_userthread",
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id'))
)

association_table_userdm = db.Table(
    "association_table_userdm",
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('dm_group_id', db.Integer, db.ForeignKey('dm_group.id'))
)

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable="False")
    email = db.Column(db.String, nullable="False")
    username = db.Column(db.String, nullable="False")
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
            "image_id": self.profile_image_id,
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
    messages = db.relationship("Message", back_populates="channel", cascade='delete')
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

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("message_image.id"), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)
    channel = db.relationship("Channel", back_populates="messages")
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
            "channel": self.channel.serialize_name(),
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

class Asset(db.Model):
    __tablename__ = "asset"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    base_url = db.Column(db.String, nullable=True)
    salt = db.Column(db.String, nullable=False)
    extension = db.Column(db.String, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'asset',
        'polymorphic_on': type
    }

    def __init__(self, **kwargs):
        self.create(kwargs.get("image_data"))
    
    def serialize(self):
        return {
            "id": self.id,
            "url": f"{self.base_url}/{self.salt}.{self.extension}",
            "created_at": str(self.created_at),
            "width": self.width,
            "height": self.height,
        }

    def create(self, image_data):
        try:
            # base64 string --> .png --> png
            ext = guess_extension(guess_type(image_data)[0])[1:]
            if ext not in EXTENSIONS:
                raise Exception(f"Extension {ext} not supported")

            # secure way of generating random string for image name
            salt = "".join(
                random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits
                )
                for _ in range(16)
            )

            # remove header of base64 string and open image
            img_str = re.sub("data:image/.+;base64", "", image_data)
            img_data = base64.b64decode(img_str)
            img = Image.open(BytesIO(img_data))

            self.base_url = S3_BASE_URL
            self.salt = salt
            self.extension = ext
            self.width = img.width
            self.height = img.height
            self.created_at = datetime.datetime.now()

            img_filename = f"{salt}.{ext}"
            self.upload(img, img_filename)
        except Exception as e:
            print(f"Unable to create image due to {e}")

    def upload(self, img, img_filename):
        try:
            img_temploc = f"{BASE_DIR}/{img_filename}"
            img.save(img_temploc)

            # upload image to S3
            s3_client = boto3.client("s3")
            s3_client.upload_file(img_temploc, S3_BUCKET, img_filename)

            # make S3 image url public
            s3_resource = boto3.resource("s3")
            object_acl = s3_resource.ObjectAcl(S3_BUCKET, img_filename)
            object_acl.put(ACL="public-read")

            os.remove(img_temploc)

        except Exception as e:
            print(f"Unable to upload image due to {e}")
    
    def delete(self):
        try: 
            img_filename = f"{self.salt}.{self.extension}"
            s3_resource = boto3.resource("s3")
            print(f"Image File Name: {self.file_name}")
            img_obj = s3_resource.Object(S3_BUCKET, img_filename)
            img_obj.delete()
        except Exception as e:
            print(f"Unable to delete image due to {e}")

class MessageImage(Asset):
    __tablename__ = 'message_image'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    source = db.Column(db.String, nullable=False) # Message or Thread
    source_id = db.Column(db.String, nullable=False)
    workspace_id = db.Column(db.Integer, db.ForeignKey("workspace.id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'message_image',
    }

    def __init__(self, **kwargs):
        self.create(kwargs.get("image_data"))
        self.sender_id = kwargs.get("sender_id")
        self.source = kwargs.get("source")
        self.source_id = kwargs.get("source_id")
        self.channel_id = kwargs.get("channel_id")
        self.workspace_id = kwargs.get("workspace_id")
    
    def serialize(self):
        return {
            "id": self.id,
            "url": f"{self.base_url}/{self.salt}.{self.extension}",
            "sender_id": self.sender_id,
            "created_at": str(self.created_at),
            "width": self.width,
            "height": self.height,
            "source": self.source,
            "source_id": self.source_id,
        }
    
    def serialize_for_message(self):
        return {
            "id": self.id,
            "url": f"{self.base_url}/{self.salt}.{self.extension}",
            "sender_id": self.sender_id,
            "created_at": str(self.created_at),
            "width": self.width,
            "height": self.height
        }

class ProfileImage(Asset):
    __tablename__ = 'profile_image'
    id = db.Column(db.Integer, db.ForeignKey('asset.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    __mapper_args__ = {
        'polymorphic_identity':'profile_image',
    }

    def __init__(self, **kwargs):
        self.create(kwargs.get("image_data"))
        self.user_id =kwargs.get("user_id")
