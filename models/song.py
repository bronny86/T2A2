from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from init import db

Base = declarative_base()

class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    format = db.Column(db.String, nullable=False)
    bpm = db.Column(db.Integer, nullable=False)
    key = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='songs')
    songlists = relationship('SongList', back_populates='song')

    # Deferred relationship definition
from models.songlist import Songlist
Song.songlists = relationship('Songlist', back_populates='song')