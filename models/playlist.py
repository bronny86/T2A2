from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from init import db

Base = declarative_base()

class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    created = db.Column(db.Date, nullable=False)
    vibe = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='playlists')
    songlists = relationship('Songlist', back_populates='playlist')