from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from init import db
from models.song import Song
from schemas.song_schema import song_schema, songs_schema

songs_bp = Blueprint("songs", __name__, url_prefix="/songs")

# /songs/ - GET - fetch all songs
@songs_bp.route("/", methods = ['GET'])
def get_all_songs():
    stmt = db.select(Song).order_by(Song.id)
    songs = db.session.scalars(stmt)
    return jsonify(songs_schema.dump(songs))

# fetch one song using song_id - GET <int> = dynamic route
@songs_bp.route("/<int:song_id>", methods = ['GET'])
def get_song(song_id):
    stmt = db.select(Song).filter_by(id=song_id)
    song = db.session.scalar(stmt)
    if song:
        return jsonify(song_schema.dump(song))
    else:
        return {"error": f'Song not found for id {song_id}'}, 404
    
# create new song model instance - POST
@songs_bp.route("/", methods = ['POST'])
@jwt_required()
def create_song():
    body_data = request.get_json()
    song = Song(
        song_name=body_data['song_name'],
        artist=body_data['artist'],
        format=body_data['format'],
        bpm=body_data['bpm'],
        key=body_data['key'],
        user_id=get_jwt_identity()
    )

    db.session.add(song)
    db.session.commit()

    return jsonify(song_schema.dump(song)), 201

@songs_bp.route("/<int:song_id>", methods = ['DELETE'])
@jwt_required()
def delete_song(song_id):
    stmt = db.select(Song).filter_by(id=song_id)
    song = db.session.scalar(stmt)
    if song:
        db.session.delete(song)
        db.session.commit()
        return {"message": f"Song '{song_id}' deleted successfully"}, 200
    else:
        return {"error": f'Song not found for id {song_id}'}, 404
    
# /songs/<id> - PUT/ PATCH update a song
@songs_bp.route("/<int:song_id>", methods = ['PUT', 'PATCH'])
@jwt_required()
def update_song(song_id):
    body_data = song_schema.load(request.get_json(), partial=True)

    stmt = db.select(Song).filter_by(id=song_id)
    song = db.session.scalar(stmt)

    if song:
        body_data = request.get_json()
        song.song_name = body_data['song_name']
        song.artist = body_data['artist']
        song.format = body_data['format']
        song.bpm = body_data['bpm']
        song.key = body_data['key']
        db.session.commit()
        return jsonify(song_schema.dump(song))
    else:
        return {"error": f'Song not found for id {song_id}'}, 404