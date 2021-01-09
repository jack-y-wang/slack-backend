from app import db
from app.models.association_tables import *

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

EXTENSIONS = ["png", "gif", "jpg", "jpeg"]

BASE_DIR = os.getcwd()

S3_BUCKET = "slack-backend-images"
S3_BASE_URL = f"https://{S3_BUCKET}.s3-us-west-1.amazonaws.com"

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
