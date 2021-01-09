from app import db

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
