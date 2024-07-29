from init import ma

class SonglistSchema(ma.Schema):

    class Meta:

        ordered = True

        fields = ("id", "playlist_id", "song_id")

songlist_schema = SonglistSchema()

songlists_schema = SonglistSchema(many=True)