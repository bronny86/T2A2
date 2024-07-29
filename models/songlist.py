from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from init import db

Base = declarative_base()

class Songlist(db.Model):
    __tablename__ = "songlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    album = db.Column(db.String, nullable=False)
    song_id = db.Column(db.Integer, ForeignKey('songs.id'))
    playlist_id = db.Column(db.Integer, ForeignKey('playlists.id'))

    song = relationship('Song', back_populates='songlists')
    playlist = relationship('Playlist', back_populates='songlists')

# Deferred relationship definition
from models.playlist import Playlist
Songlist.playlist = relationship('Playlist', back_populates='songlists')