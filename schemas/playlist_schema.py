from init import ma

from marshmallow import fields

class PlaylistSchema(ma.Schema):
        user = fields.Nested('UserSchema', only=["id", "username", "email"])
        songs = fields.List(fields.Nested('SongSchema', exclude=["playlist"]))

        class Meta:
            fields = ("id", "title", "created", "vibe", "user")
            ordered = True

playlist_schema = PlaylistSchema()
    
playlists_schema = PlaylistSchema(many=True)