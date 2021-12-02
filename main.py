from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mypassword@localhost/auction'
db = SQLAlchemy(app)

class Users(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Namn = db.Column(db.String(30), unique=False, nullable=False)
    Address = db.Column(db.String(100), unique=False, nullable=False)
    Username = db.Column(db.String(30), unique=False, nullable=False)
    Password = db.Column(db.String(30), unique=False, nullable=False)

    Annonsers =  db.relationship('Annonser', backref='Users', lazy=True)


class Anonsers(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(50), unique=False, nullable=False)
    Description = db.Column(db.String(300), unique=False, nullable=False)
    StartPrice = db.Column(db.Integer, unique=False, nullable=True)
    StartDateTime = db.Column(db.Datetime, unique=False, nullable=True)
    EndDateTime = db.Column(db.Datetime, unique=False, nullable=True)
    Bild_Id = db.Column(db.Integer, db.ForeignKey('Bilder.Id'), unique=False, nullable=True)
    User_Id = db.Column(db.Integer, db.ForeignKey('Users.Id'), unique=False, nullable=True)


class Bilder(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(100), unique=False, nullable=False)
    Description = db.Column(db.String(300), unique=False, nullable=True)

    Annonsers =  db.relationship('Annonser', backref='Bilder', lazy=True)
