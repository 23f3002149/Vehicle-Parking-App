from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()




# here i am writing the data models.
#here we are going to create all data models with all the relationship ofprimary key and all other stuff

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()#here i am creating instance(object) of the database , Creating an instance of the database means setting up and initializing a specific database that can be used for storing and managing data.
#In practical terms, it refers to:

# Establishing a Connection: Connecting your application to a database server (e.g., SQLite, MySQL, PostgreSQL).
# Creating Database Objects: Defining tables, columns, relationships, and constraints.
# Allocating Storage: Setting up space in memory or disk for storing data.
# Initializing with Data (Optional): Pre-populating tables with required records (e.g., adding an admin user by default).

# creating first entity(first_table)
# class User(db.Model): Defines a table named user.
# db.Column(...): Defines columns in the table.
#db = SQLAlchemy(app) you will write this if and only if models.py is combined in app.py

class Admin_User_Details(db.Model):
    __tablename__ = 'admin_user_details'
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)#Ensures that the ID column automatically increments for each new row inserted into the table.The database automatically assigns a new unique ID starting from 1 and increases by 1 for each new entry.
    email=db.Column(db.String(50),nullable=False,unique=True)# unique to hoga hi
    full_name=db.Column(db.String(50),nullable=False)#not neccessary to be unique
    password=db.Column(db.String(50),nullable=False)#not neccessary to be unique# here string(50) means 50 characters
    address=db.Column(db.String(120),nullable=False)#not neccessary to be unique
    pincode=db.Column(db.Integer,nullable=False)#not neccessary to be unique
    role=db.Column(db.Integer,nullable=False,default=1)#not neccessary to be unique
     # relations with other tables(backrefrencing means getting all child infromation through parent )we will write later,,,,haaa now it is written below
    Reserved_parking_spots_of_a_user_id=db.relationship('Reserved_parking_spots',backref='admin_user_details' , cascade='all , delete' , lazy=True)#it tells all the reserved parking spots of a particular user

class Parking_Lots(db.Model):
    __tablename__ = 'parking_lots'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    prime_location_name=db.Column(db.String(50),nullable=False ,unique=True)#location name jo ki parking lot ka name hoga vo to alag hi hona chahiye
    address=db.Column(db.String(120),nullable=False)#not neccessary to be unique ,aisa ho sakta hai demand ki vajah se ek hi city me 2 parking lot honge
    pincode=db.Column(db.Integer,nullable=False)#not neccessary to be unique
    price_per_spot_per_hour=db.Column(db.Integer,nullable=False)#not neccessary to be unique
    max_spots=db.Column(db.Integer,nullable=False)#not neccessary to be unique
    # relations with other tables(backrefrencing means getting all child infromation through parent )we will write later,,,,haaa now it is written below
    parking_spots_of_a_lot_id=db.relationship('Parking_Spots',backref='parking_lots' , cascade='all , delete' , lazy=True)#it tells all the parking spots of a particular lot(here we are gettting parking lot by lot id)

    Reserved_parking_spots_of_a_lot_id=db.relationship('Reserved_parking_spots',backref='parking_lots' , cascade='all , delete' , lazy=True)#it tells all the reserved parking spots of a particular lot


class Parking_Spots(db.Model):
    __tablename__ = 'parking_spots'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    lot_id=db.Column(db.Integer,db.ForeignKey('parking_lots.id'), nullable=False)
    status=db.Column(db.String(50),nullable=False)
    # relations with other tables(backrefrencing means getting all child infromation through parent )we will write later,,,,haaa now it is written below
    reserved_parking_spot_of_the_spot_id=db.relationship('Reserved_parking_spots',backref='parking_spots' , cascade='all , delete' , lazy=True)#it tells all the reserved parking spots of a particular spot

class Reserved_parking_spots(db.Model):#this table is for the reservation(booking) of the parking spot
    __tablename__ = 'reserved_parking_spots'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    spot_id=db.Column(db.Integer,db.ForeignKey('parking_spots.id'), nullable=False)
    lot_id=db.Column(db.Integer,db.ForeignKey('parking_lots.id'), nullable=False)
    user_id=db.Column(db.String(50),db.ForeignKey('admin_user_details.email'), nullable=False)
    vehicle_number=db.Column(db.String(50),nullable=False)
    parking_timestamp=db.Column(db.DateTime,nullable=False)
    leaving_timestamp=db.Column(db.DateTime,nullable=True)
    parking_price_per_hour=db.Column(db.Integer,nullable=False)#isko to mai parking lot walli table se hi le lunga ....
    # relations with other tables(backrefrencing means getting all child infromation through parent )we will write later,,,,haaa now it is written below
    # relations with other tables(backrefrencing means getting all child infromation through parent )we will write later,,,,haaa now it is written below
