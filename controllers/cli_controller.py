from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.playlist import Playlist
from models.song import Song


db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command("seed")
def seed_tables():
    # create a list of User instances
    users = [
        User(
            email="admin@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            is_admin=True
        ),

        User(
            name='Dan Watt',
            email='wattsonpresents@gmail.com',
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        ),
        User(
            name='Percy Colthurst',
            email= 'percy@postpercy.com',
            password=bcrypt.generate_password_hash('123456').decode('utf-8')
        ),
        User(
            name ='Minky Binky',
            email='minky@kitten.com',
            password=bcrypt.generate_password_hash('123456').decode('utf-8')

        ),
        User(
            name= 'Bootsy Watt',
            email= 'bootsy@kittylinks.com',
            password= bcrypt.generate_password_hash('123456').decode('utf-8')
        )
        
    ]

    db.session.add_all(users)

    playlists = [
        Playlist(
            title='Minky Faves',
            created = date.today(),
            vibe = 'Fun Dancey',
            user = users[2],

        ),
        Playlist(
            title='Late Night',
            created = date.today(),
            vibe= 'Chill Beats',
            user =users[3],
        ),
        Playlist(
            title = 'Last Chance DJ Set',
            created = date.today(),
            vibe = 'Punk',
            user = users[0],
        ),
        Playlist(
            title = 'Retro',
            created = date.today(),
            vibe = '80s',
            user = users[2],
        ),
        Playlist(
            title = 'Tasteful Dance',
            created = date.today(),
            vibe = 'Tasteful House',
            user = users[3],
        ),
        Playlist(
            title = 'Leonards DJ Set',
            created = date.today(),
            vibe = 'Rock',
            user = users[1],
        )
    ]

    db.session.add_all(playlists)


    songs =[
        Song(
            title ='TKO',
            artist = 'Le Tigre',
            format = 'CD',
            bpm = '139',
            key = 'E',
        ),

        Song(
            title = 'Sabotage',
            artist = 'Beastie Boys',
            format = 'vinyl',
            bpm = '168',
            key = 'F',
    
        ),
        Song(
            title = 'I Love Livin In The City',
            artist = 'Fear',
            format = 'cd',
            bpm = '105',
            key = 'F',
        ),
        Song(
            title = 'Blue Monday',
            artist = 'New Order',
            format = 'vinyl',
            bpm = '130',
            key = 'C',
        
        ),
        Song(
            title = 'Killing in the Name of',
            artist = 'Rage Against The Machine',
            format = 'iTunes',
            bpm = '88',
            key = 'G',
            
        ),
        Song(
            title = 'Last Night',
            artist = 'The Strokes',
            format = 'USB',
            bpm = '104',
            key = 'C',
            
        ),
        Song(
            title ='Love Cats',
            artist = 'The Cure',
            format = 'vinyl',
            bpm = '92',
            key = 'A',
            
        ),
        Song(
            title = 'Spiderwebs',
            artist = 'No Doubt',
            format = 'iTunes',
            bpm = '143',
            key = 'B',
           
        ),
        Song(
            title = 'Head Like A Hole',
            artist = 'Nine Inch Nails',
            format = 'USB',
            bpm = '115',
            key = 'G',
        
        ),
        Song(
            title = 'Epic',
            artist = 'Faith No More',
            format = 'CD',
            bpm = '87',
            key = 'G',
        
        ),
        Song(
            title = 'Steal My Sunshine',
            artist = 'LEN',
            format = 'iTunes',
            bpm = '96',
            key = 'E',
            
        ),
        Song(
            title = 'Semi-Charmed Kinda Life',
            artist = 'Third Eye Blind',
            format = 'CD',
            bpm = '102',
            key = 'G',
        
        ),
        Song(
            title = 'Boys Wanna Be Her',
            artist = 'Peaches',
            format = 'CD',
            bpm = '139',
            key = 'G',
            
        ),
        Song(
            title = 'Volcano Girls',
            artist = 'Veruca Salt',
            format = 'vinyl',
            bpm = '131',
            key = 'D',
           

        ),
        Song(
            title = 'Psycho Killer',
            artist = 'Talking Heads',
            format = 'vinyl',
            bpm = '123',
            key = 'C',
            
        ),
        Song(
            title = 'Edge of Seventeen',
            artist = 'Stevie Nicks',
            format = 'vinyl',
            bpm = '111',
            key = 'G',
           
        )
        
    ]
    db.session.add_all(songs)

    db.session.commit()

    print("Tables seeded")