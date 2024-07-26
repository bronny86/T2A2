from init import db, ma
from marshmallow import fields


class Song(db.Model):
    # name of the table
    __tablename__ = "songs"

    # attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    artist =db.Column(db.String)
    format = db.Column(db.String)
    bpm = db.Column(db.String)
    key = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # connecting to foregin key in playlist
    user = db.relationship('User', back_populates='song')