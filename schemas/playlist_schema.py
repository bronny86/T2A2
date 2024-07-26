from init import db, ma

from marshmallow import fields

class PlaylistSchema(ma.Schema):
        user = fields.Nested('UserSchema', only=["id", "name", "email"])

        class Meta:
            fields = ("id", "title", "created", "vibe", "user")
            ordered = True

playlist_schema = PlaylistSchema()
    
playlists_schema = PlaylistSchema(many=True)