from init import ma
from marshmallow import fields

class SongSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=["id", "username", "email"])

    class Meta:
         fields = ("id", "song_name", "artist", "format", "bpm", "key", "user" )

         ordered = True

    songlist = fields.Nested("SonglistSchema")

song_schema = SongSchema()
songs_schema = SongSchema(many=True)