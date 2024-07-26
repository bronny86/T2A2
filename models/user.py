from init import db, ma
from marshmallow import fields


class User(db.Model):
    # name of the table
    __tablename__ = "users"

    # attributes of the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # connecting to foregin key in playlist
    playlists = db.relationship('Playlist', back_populates="user")
    songs = db.relationship('Song', back_populates="user")

class UserSchema(ma.Schema):

# is playlistS because one user can have many playlists
    playlists = fields.List(fields.Nested('PlaylistSchema', exclude=["user"]))

    songs = fields.List(fields.Nested('SongSchema', exclude=["user"]))

    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "playlists", "songs")


# to handle a single user object
user_schema = UserSchema(exclude=["password"])

# to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])