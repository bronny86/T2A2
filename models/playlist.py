from init import db, ma
from marshmallow import fields

from schemas.playlist_schema import PlaylistSchema, playlist_schema, playlists_schema

class Playlist(db.Model):

    __tablename__="playlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    created = db.Column(db.Date)
    vibe = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='playlists')