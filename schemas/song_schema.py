from init import ma
from marshmallow import fields

class SongSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["id", "username", "email"])
    playlist = fields.Nested('PlaylistSchema', only=["id", "title"])

    class Meta:
         fields = ("id", "song_name", "artist", "format", "bpm", "key", "user", "playlist" )

         ordered = True

    songlist = fields.Nested("SonglistSchema")

song_schema = SongSchema()
songs_schema = SongSchema(many=True)