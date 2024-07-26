from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from init import db
from models.playlist import Playlist
from schemas.playlist_schema import playlist_schema, playlists_schema

playlists_bp = Blueprint("playlists", __name__, url_prefix="/playlists")

# /playlist/ - GET - fetch all playlists
@playlists_bp.route("/", methods = ['GET'])
def get_all_playlists():
    stmt = db.select(Playlist).order_by(Playlist.created.desc())
    playlists = db.session.scalars(stmt)
    return playlists_schema.dump(playlists)

# fetch one playlist using playlist_id - GET <int> = dynamic route
@playlists_bp.route('<int:playlist_id>', methods = ['GET'])
def get_one_playlist(playlist_id):
    stmt = db.select(Playlist).filter_by(id=playlist_id)
    playlist = db.session.scalar(stmt)
    if playlist:
        return playlist_schema.dump(playlist)
    else:
        return {'error': f'Playlist not found with id {playlist_id}'}, 404
    
# create new playlist model instance - POST
@playlists_bp.route('/', methods = ['POST'])
@jwt_required()
def create_playlist():
    body_data = request.get_json()
    playlist = Playlist(
        title = body_data.get('title'),
        created =date.today(),
        vibe = body_data.get('vibe'),
        user_id=get_jwt_identity()
    )
    
    db.session.add(playlist)
    db.session.commit()

    return playlist_schema.dump(playlist), 201

# /playlists/<id> - DELETE - delete a playlist

@playlists_bp.route("/<int:playlist_id>", methods=["DELETE"])
@jwt_required()
def delete_playlist(playlist_id):
    # fetch the playlist from database
    stmt = db.select(Playlist).filter_by(id=playlist_id)
    # if playlist exists
    playlist = db.session.scalar(stmt)
    if playlist:
        # delete the playlist
        db.session.delete(playlist)
        db.session.commit()
        return {"message": f"Playlist '{playlist.title}' deleted successfully"}
    # else return error
    else:
        return {"error": f"Playlist with id {playlist_id} not found"}, 404

# /playlists/<id> - PUT PATCH - edit a playlist
    
@playlists_bp.route("/<int:playlist_id>", methods =["PUT", "PATCH"])
@jwt_required()
def update_playlist(playlist_id):
    # get the data from body of the request
    body_data = request.get_json()
    # get the playlist from the database
    stmt = db.select(Playlist).filter_by(id=playlist_id)
    playlist = db.session.scalar(stmt)
    # if playlist exists
    if playlist:
        # update fields as required
        playlist.title = body_data.get("title") or playlist.title
        playlist.vibe = body_data.get("vibe") or playlist.vibe
        # commit to db
        db.session.commit()
        # return a response
        return playlist_schema.dump(playlist)
    # else
    else:
        # return an error
        return {"error": f"Playlist with id {playlist_id} not found"}, 404