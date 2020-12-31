from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

# association_table_userthread = db.Table(
#     "association_table_userthread",
#     db.Model.metadata,
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('message_id', db.Integer, db.ForeignKey('message.id'))
# )

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable="False")
    email = db.Column(db.String, nullable="False")
    username = db.Column(db.String, nullable="False")
    workspaces = db.relationship(
        "Workspace", 
        secondary=association_table_userworksp,
        back_populates="users"
    )
    # threads = db.relationship(
    #     "Message",
    #     back_populates="users_following"
    # )

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "workspaces": [w.serialize() for w in self.workspaces]
        }
    
    def serialize_name(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username
        }


class Workspace(db.Model):
    __tablename__ = "workspace"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    channels = db.relationship("Channel", cascade="delete", back_populates="workspace")
    users = db.relationship(
        "User", 
        secondary=association_table_userworksp,
        back_populates="workspaces"
    )

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
    workspace = db.relationship("Workspace", back_populates="channels")
    users = db.relationship(
        "User",
        secondary=association_table_userchannel
    )
    messages = db.relationship("Message", back_populates="channel")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")
        self.public = kwargs.get("public")
        self.workspace_id = kwargs.get("workspace_id")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "workspace": self.workspace.serialize_name(),
            "users": [u.serialize_name() for u in self.users],
            "messages": [m.serialize_content() for m in self.messages] 
        }
    
    def serialize_name(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": [u.serialize_name() for u in self.users]
        }

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)
    channel = db.relationship("Channel", back_populates="messages")
    threads = db.relationship("Thread", back_populates='message', cascade='delete')
    # users_following = db.relationship("User", back_populates='threads')
    updated = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.sender_id = kwargs.get("sender_id")
        self.content = kwargs.get("content")
        self.timestamp = kwargs.get("timestamp")
        self.channel_id = kwargs.get("channel_id")
        self.updated = False
    
    def serialize(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "timestamp": str(self.timestamp),
            "channel": self.channel.serialize_name(),
            "threads": [t.serialize_content() for t in self.threads],
            # "users_following": self.users_following.serialize_name(),
            "updated": self.updated
        }
    
    def serialize_content(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
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
    updated = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        self.sender_id = kwargs.get("sender_id")
        self.content = kwargs.get("content")
        self.timestamp = kwargs.get("timestamp")
        self.message_id = kwargs.get("message_id")
        self.updated = False
    
    def serialize(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "timestamp": str(self.timestamp),
            "message": self.message.serialize_content(),
            "updated": self.updated
        }
    
    def serialize_content(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "timestamp": str(self.timestamp),
            "updated": self.updated
        }
