from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from init import db
from models.song import Song
from schemas.song_schema import song_schema, songs_schema

songs_bp = Blueprint("songs", __name__, url_prefix="/songs")

# /song/ - GET - fetch all songs
@songs_bp.route("/", methods = ['GET'])
def get_all_songs():
    stmt = db.select(Song)
    songs = db.session.scalars(stmt)
    return songs_schema.dump(songs)

# fetch one song using song_id - GET <int> = dynamic route
@songs_bp.route('<int:song_id>', methods = ['GET'])
def get_one_song(song_id):
    stmt = db.select(Song).filter_by(id=song_id)
    song = db.session.scalar(stmt)
    if song:
        return song_schema.dump(song)
    else:
        return {'error': f'Song not found with id {song_id}'}, 404
    
# create new song model instance - POST
@songs_bp.route('/', methods = ['POST'])
@jwt_required()
def create_song():
    body_data = request.get_json()
    song = Song(
        title = body_data.get('title'),
        artist = body_data.get('artist'),
        format = body_data.get('format'),
        bpm = body_data.get('bpm'),
        key = body_data.get('key'),
        user_id=get_jwt_identity(),
        )
    
    db.session.add(song)
    db.session.commit()

    return song_schema.dump(song), 201

# /song/<id> - DELETE - delete a song

@songs_bp.route("/<int:song_id>", methods=["DELETE"])
@jwt_required()
def delete_song(song_id):
    # fetch the playlist from database
    stmt = db.select(Song).filter_by(id=song_id)
    # if song exists
    song = db.session.scalar(stmt)
    if song:
        # delete the song
        db.session.delete(song)
        db.session.commit()
        return {"message": f"Song '{song.title}' deleted successfully"}
    # else return error
    else:
        return {"error": f"Song with id {song_id} not found"}, 404

# /songs/<id> - PUT PATCH - edit a song
    
@songs_bp.route("/<int:song_id>", methods =["PUT", "PATCH"])
@jwt_required()
def update_song(song_id):
    # get the data from body of the request
    body_data = request.get_json()
    # get the playlist from the database
    stmt = db.select(Song).filter_by(id=song_id)
    song = db.session.scalar(stmt)
    # if playlist exists
    if song:
        # update fields as required
        song.title = body_data.get("title") or song.title
        song.artist = body_data.get("artist") or song.artist
        song.format = body_data.get("format") or song.format
        song.bpm = body_data.get("bpm") or song.bpm
        song.key = body_data.get("key") or song.key
        # commit to db
        db.session.commit()
        # return a response
        return song_schema.dump(song)
    # else
    else:
        # return an error
        return {"error": f"Song with id {song_id} not found"}, 404