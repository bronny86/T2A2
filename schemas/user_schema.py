from init import ma

from marshmallow import fields

class UserSchema(ma.Schema):
    playlists = fields.List(fields.Nested('PlaylistSchema', exclude=["user"]))
    songs = fields.List(fields.Nested('SongSchema', exclude=["user"]))

    class Meta:
        fields = ("id", "username", "email", "password", "is_admin", "playlists", "songs")
        ordered = True

# to handle a single user object
user_schema = UserSchema(exclude=["password"])

# to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])
