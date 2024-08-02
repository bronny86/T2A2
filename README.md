# T2A2 MUSIC LIBRARY API

### [GitHub Repo](https://github.com/bronny86/T2A2)

### Installation and Setup

- Creater a folder locally to store the API
- Clone or download the repository from Github

Connect to PostgresSQL database from Flask by running this in the terminal

```
`psql`
```

Then create the database and name it library_db, create a user named library_dev with password 123456 and grant this user all privileges

```
CREATE DATABASE library_db;
\c library_db;
CREATE USER library_dev WITH PASSWORD '123456'
GRANT ALL PRIVILEGES ON DATABASE library_db TO library_dev;
```

Open the src folder from the Github repo downloaded earlier and create a virtual environment by entering:

```
python3 -m venv . venv
```

then activate the virtual environment:

```
source .venv/bin/activate
```

Install required packages:

```
pip3 install -r requirements.txt
```

At the root directory create an .env file and enter:

```
DATABASE_URI=“postgresql+psycopg2://library_dev:123456@localhost:5432/library_db"
JWT_SECRET_KEY="secret"
```

Finally create and seed the database and then run Flask by entering:

```
flask db create
flask db seed
flask run
```

### R1. Explain the problem that this app will solve, and explain how this app solves or addresses the problem.

The problem I aim to solve with this app is the issue encountered particularly by DJs (but could also apply to anybody with a large music library in a variety of formats) where their music library is often spread out across many different formats - vinyl, CDs, USBs, iTunes and other online platforms. By entering their music library into the app the user is able to easily see what format they own each song in, and also what key each song is in and what BPM. Users can also create and store their own playlists.

### R2. Describe the way tasks are allocated and tracked in your project.

### R3. List and explain the third-party services, packages and dependencies used in this app.

###### dotenv

Programmers have the ability to import environment variables from a file named ".env" located in the project directory by utilizing the Python module Python-Dotenv. This library facilitates the management of environment variables by allowing programmers to separate confidential data from their code and easily switch between different environment setups.

###### JWT-Extended
Flask-JWT-Extended adds support for using JSON Web Tokens (JWT) to Flask for protecting routes.

###### Flask Bcrypt
Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities. it is uesd in the API for storing passwords of users securly.

###### Marshmallow

Marshmallow is a Python package that facilitates the conversion of intricate data kinds to and from Python data types. It is a potent instrument for both verifying and transforming data.

The Python code facilitates the conversion of data from database tables into JSON format, which may subsequently be sent via API endpoints. Flask-Marshmallow generates the JSON data returned by the API endpoints by defining schema classes that match the database tables. Consequently, the API provides a consistent and unambiguous data format that can be utilized by other programs and services.

###### Psycopg2

Psycopg2 is a multi-threaded application that serves as a PostgreSQL database driver for conducting operations on PostgreSQL using Python. The execute() function in psycopg2 is utilized to execute SQL queries. It is utilized to execute a database action, command, or query.

Psycopg2 is a Python library that facilitates the establishment of connections with PostgreSQL databases and enables the execution of CRUD (Create, Read, Update, Delete) actions on the tables inside the database. It enables the Python code to communicate with the database by utilizing SQL commands, such as SELECT, INSERT, UPDATE, and DELETE.

### R4. Explain the benefits and drawbacks of this app’s underlying database system.

I used PostgreSQL to create and manipulate a relational database. One of the most popular RDBMSs, PostgreSQL has various database construction and maintenance functions. Its reliability and capacity to handle massive amounts of data and traffic without affecting application performance or data integrity make it a good choice for this application.

PostgreSQL supports developing database functions in the API webserver's primary languages, SQL and Python, which is one of its fundamental advantages. PostgreSQL supports numeric, Boolean, and string database primitives needed to develop applications. Since JSON will be used to design and create this application, its support for JSON makes it a good choice for relational data. Defining my own kinds and transmitting data for the web application will help me structure and develop my database.

Any application needs authentication, access control, and security. PostgreSQL offers a sophisticated framework to handle these aspects efficiently. Authentication and authorization are essential for personal data. PostgreSQL has authentication, role-based access control, encryption, and permissions. These are essential to establishing a secure application and protecting user data.

Another PostgreSQL feature is the ability to construct inheritance connections between tables and add comments. Table inheritance simplifies indexes and speeds database searches. For a cascading effect on other tables, only the parent table needs to be modified, making changes easy. Database management benefits from these smaller indexes, which make reading and organization easier. Adding comments to tables, databases, and other database objects helps organize and manage application data.

With its many features, reliability, performance, and community support, it's ideal for building this app. Wide community support makes PostgreSQL a pleasant and well-documented platform, adding to its benefits. Its community popularity and regular updates and bug fixes make it a good choice for this application.

###### What's the downside compared to others?

Due to its extensive and complicated capabilities, PostgreSQL can be difficult for newcomers. Lack of system expertise might affect performance owing to learning curve and database organization. Since hosting platforms don't install it, you must. Further installation of external resources is another problem since PostgreSQL lacks standard tools found in other DBMSs.

To cache data and perform searches efficiently with massive amounts of data, RAM is needed. Without enough storage, this affects system performance. Low reading speeds due to application size can also affect performance. Due to its lack of compression, large loading procedures hinder performance.

### R5. Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.

Object Relational Mapping (ORM) is a component that connects objects in programming languages (specifically Python classes/models) to a corresponding database (in this project, PostgresQL is used as the database management system). This allows for easy development of associations and efficient execution of SQL operations. There are numerous advantages to employing Object-Relational Mapping (ORM) techniques, which encompass:

ORMs facilitate faster code development by reducing the necessity for excessive coding through their capability to translate SQL queries.

DRY coding refers to the practice of establishing models in one place and reusing them throughout the program, eliminating the need to duplicate characteristics.
Facilitates the process of verifying and cleaning.
From a developer's standpoint, a comprehensive understanding of the database management system is not necessary as ORMs handle the tasks.

### R6. Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. 

###### This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.

![originalERD](/docs/originalERD.png)

This was my original ERD that I created prior to beginning actually coding etc. In this ERD I had songs connected to users in a one to one or many (one user can have zero or many song, one song can only have one user). I wanted to have a many-to-many relationship between songs and playlists (one song can be in many playlists, playlists can have many songs) so I represented this by using the Songs_Playlists table as a joining table holding the Foreign Keys of Playlist_ID and Song_ID. In this original ERD I included a lot of fields in the Songs table that I later decided wasn’t really necessary such as Year Released, Song Length, and Genre which I ended up moving to the Playlists table later on as ‘vibe’.

### R7. Explain the implemented models and their relationships, including how the relationships aid the database implementation.

##### This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.

![finalERD](/docs/ERD-Final.jpeg)

This is a final ERD representing how my models and relationships ended up after various issues etc cropped up once I actually began coding.

I moved the tables around so that the User table was connected to both the Playlists and Songs tables with one-to-one-or-many relationships (one users can have many songs, one user can have many playlists, each song may only have one user, each playlist may only have one user) which meant that I was able to list each user and their assoicated songs and playlists. I cut down the fields included in the Song table to just song name, artist, bpm and key and edited the fields in the Playlist table to title, date created and vibe. I changed the name of the Songs_Playlists table to ‘Songlist’ but it’s function remained the same, as a joining table between the Songs and Playlists tables that just stored the Foreign Keys.

### R8. Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:

### User End Points

![usersendpoints1](/docs/users%20CRUD%201.png)
![usersendpoints2](/docs/users%20CRUD%202.png)

###### ‘/auth/register’

![register](/docs/Admin%20can%20create%20new%20user.png)

POST method to register new user. JSON body required.

###### ‘/auth/login’

![login](/docs/Auth%20Login.png)

POST method for existing users to login. JSON body required.

###### ‘/users’

![listusers](/docs/Admin%20can%20fetch%20list%20of%20all%20users.png)

GET method to list all registered users. Admin only, Bearer token required.

###### ‘/users/<int:id>/‘

![adminoneuser](/docs/Admin%20can%20search%20user%20by%20ID.png)

GET method to fetch one user by user ID. Admin only, Bearer token required.

###### ‘/users/<int:id>/‘

![usersedit](/docs/Users%20can%20edit%20their%20own%20profile.png)

![userediterror](/docs/user%20edit%20ERROR.png)

PUT method for users to edit their own profile. Users may only edit their own profile, Bearer token required, JSON body.

###### ‘/users/<int:id>/‘

![admindelete](/docs/Admin%20can%20DELETE%20user.png)

DELETE method to delete user. Admin only, Bearer token required.

### Playlist End Points

![playlists](/docs/playlists%20CRUD.png)

###### ‘/playlists/‘

![allplaylists](/docs/GET%20fetch%20all%20playlists.png)

GET method to get list of all playlists.

###### ‘/playlists/<int:id>

![oneplaylist](/docs/GET%20fetch%20one%20playlist%20by%20ID.png)

GET method to get one playlist by playlist ID.

###### ‘/playlists’

![newplaylist](/docs/POST%20create%20new%20playlist.png)

POST method to create new playlist. JSON body and Bearer token required.

###### ‘/playlists/<int:id>/‘

![deleteplaylist](/docs/DELETE%20delete%20playlist%20by%20ID.png)

DELETE method to delete one playlist. Users can only delete their own playlists. Bearer token required.

###### ‘/playlists/<int:id>/‘

![editplaylist](/docs/PATCH%20edit%20playlist.png)

PATCH method users can edit their own playlists. JSON body and Bearer token required.

### Song End Points

![songs](/docs/songs%20CRUD.png)

###### ‘/songs’

![allsongs](/docs/GET%20fetch%20all%20songs.png)

GET method, get a list of all songs.

###### ‘/songs/<int:id>’

![onesong](/docs/GET%20fetch%20one%20song%20by%20id.png)

![getsongerror](/docs/songs%20ERROR.png)

GET method, get one song by song ID

###### ‘/songs/‘

![createnewsong](/docs/POST%20create%20new%20song.png)

POST method, create/add new song. JSON body, Bearer token required.

###### ‘/songs/<int:id>/‘

![deletesong](/docs/DELETE%20delete%20one%20song%20by%20id.png)

DELETE method, delete one song by ID. Users can only delete thier own songs, bearer token required.

###### ‘/songs/<int:id>/‘

![editsong](/docs/PATCH%20edit%20one%20song%20by%20ID.png)

PATCH method users can edit their own songs. JSON body, bearer token required.

![createseed](/docs/create%20seed.png)

![dt](/docs/dt.png)

![selectusers](/docs/select%20*%20from%20users.png)

![selectplaylist](/docs/select%20*%20from%20playlists.png)

![selectsong](/docs/select%20*%20from%20songs.png)