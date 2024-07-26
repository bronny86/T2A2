from init import db, ma

from marshmallow import fields

class SongSchema(ma.Schema):
        user = fields.Nested('UserSchema', only=["id", "name", "email"])

        class Meta:
            fields = ("id", "title", "artist", "format", "bpm", "key", "user")
            ordered = True

song_schema = SongSchema()
    
songs_schema = SongSchema(many=True)