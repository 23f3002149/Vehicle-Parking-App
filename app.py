

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.Models import db# from backend.models i am importing the db variable(instance of database which we have created in models.py)
# app=None

def setup_app():
    # global app
    app=Flask(__name__)
    app.secret_key = 'your_super_secret_key_123'
    app.app_context().push()
    #Pending here is sqlite connection#now my model is ready in models.py and i want to acess in my_app.py also,so i import my models from backend
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///vehicle_parking.sqlite3"###this is the path of the database#this is the file name(vehicle_parking.sqlite3) of the database which we can see in db browser,where the actual data is stored,because in models.py we have defined the database but where store our data is this instance file.
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config['SQLSCRERT_KEY'] = 'super secret key'
    db.init_app(app)#db has to be connected to the flask app so db.init_app(app) links the db instance to the Flask app so that the app knows how to manage the database.#it has established connection between db and our flask app
    #now to create instance we have to run two commands only for one time 1. type python which open python 2.now type from backend.models import db 3. type from app import *

    app.debug=True
    with app.app_context():
        db.create_all()
    print("database connected")
    return app
    

app=setup_app()

from backend.controlers import *


if __name__ == '__main__':
    app.run(debug=True)































# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from backend.models import db # Admin, User, Subject, Chapter, Quiz, Question, Score


# # db = SQLAlchemy()

# def setup_app():
#     app = Flask(__name__)

#     # SQLite database path inside the instance folder
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_system.sqlite3'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)

#     # Push app context for database initialization
#     with app.app_context():
#      db.create_all()  # Create all tables defined in the models

#     print("Database created successfully in the instance folder!")

#     return app

# # Initialize Flask app
# app = setup_app()
# from backend.controlers import *
# # Run the app if needed
# if __name__ == "_main_":
    # app.run(debug=True)




























