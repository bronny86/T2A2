from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from init import db
from models.song import Song
from models.user import User
from schemas.song_schema import SongSchema, song_schema, songs_schema

songs_bp = Blueprint("songs", __name__, url_prefix="/songs")

# /songs/ - GET - fetch all songs
@songs_bp.route("/", methods = ['GET'])
def get_all_songs():
    stmt = db.select(Song).order_by(Song.id)
    songs = db.session.scalars(stmt)
    return jsonify(songs_schema.dump(songs))