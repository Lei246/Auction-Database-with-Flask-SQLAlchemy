from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import socket
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mypassword@localhost/auction'
db = SQLAlchemy(app)

class Bilder(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    URL = db.Column(db.String(100), unique=False, nullable=False)
    Description = db.Column(db.String(300), unique=False, nullable=True)

    Anonsers =  db.relationship('Anonsers', backref='Bilder', lazy=True)

class Users(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Namn = db.Column(db.String(30), unique=False, nullable=False)
    Address = db.Column(db.String(100), unique=False, nullable=False)
    Username = db.Column(db.String(30), unique=True, nullable=False)
    Password = db.Column(db.String(30), unique=False, nullable=False)

    Anonsers =  db.relationship('Anonsers', backref='Users', lazy=True)
    Loggin =  db.relationship('Loggin', backref='Users', lazy=True)
    Bud =  db.relationship('Bud', backref='Users', lazy=True)

class Anonsers(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(50), unique=False, nullable=False)
    Description = db.Column(db.String(300), unique=False, nullable=False)
    StartPrice = db.Column(db.Integer, unique=False, nullable=True)
    StartDateTime = db.Column(db.DateTime, unique=False, nullable=True)
    EndDateTime = db.Column(db.DateTime, unique=False, nullable=True)
    Bild_Id = db.Column(db.Integer, db.ForeignKey('bilder.Id'), unique=False, nullable=True) # ForeignKey('bilder.Id') NOT ('Bilder.Id')
    User_Id = db.Column(db.Integer, db.ForeignKey('users.Id'), unique=False, nullable=False)

    Bud =  db.relationship('Bud', backref='Anonsers', lazy=True)

class Loggin(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    LogDateTime = db.Column(db.DateTime, default=datetime.now, unique=False, nullable=False)
    IPAdrress = db.Column(db.String(30), unique=False, nullable=False)
    User_Id = db.Column(db.Integer, db.ForeignKey('users.Id'), unique=False, nullable=False)

class Bud(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    BudDateTime = db.Column(db.DateTime, default=datetime.now, unique=False, nullable=False)
    NewPrice = db.Column(db.Integer, unique=False, nullable=True)
    User_Id = db.Column(db.Integer, db.ForeignKey('users.Id'), unique=False, nullable=False)
    Anonsers_Id = db.Column(db.Integer, db.ForeignKey('anonsers.Id'), unique=False, nullable=False)


db.create_all()

while True:
    print("1. Create a new user: ")
    print("2. List all the users: ")
    print("3. Create a new bild: ")
    print("4. Log in: ")
    print("5. Create a new anons: ")
    print("6. List all the anonser: ")
    print("7. Give a new(higher) bud: ")



   
    sel = int(input("Which one do you want:"))
    if sel == 1:
        u = Users()
        u.Namn = input("Ange name:")
        u.Address = input("Ange Address:")
        u.Username = input("Ange Username:")
        u.Password = input("Ange Password:")

        db.session.add(u)
        db.session.commit()        

    if sel == 2:
        for s in Users.query.all():
            print(f"{s.Id}  {s.Username}")


    if sel == 3:
        b = Bilder()
        b.URL = input("Ange URL:")
        b.Description = input("Ange description:")

        db.session.add(b)
        db.session.commit() 


    if sel == 4:
        l = Loggin()
        for s in Users.query.all():
            print(f"{s.Id}  {s.Username}")
        l.User_Id = input("choose your User_Id to log in:")
        l.IPAdrress = socket.gethostbyname(socket.gethostname())
        db.session.add(l)
        db.session.commit() 


    if sel == 5:
        a = Anonsers()
        a.Title = input("Ange title:")
        a.Description = input("Ange description:")
        a.StartPrice = input("Ange start price:")
        a.StartDateTime = input("Ange start date and time:")
        a.EndDateTime = input("Ange end date and time:")
        for s in Bilder.query.all():
            print(f"{s.Id}  {s.Description}")
        a.Bild_Id = input ("Ange bild id: ")
        for s in Users.query.all():
            print(f"{s.Id}  {s.Username}")
        a.User_Id = input ("Ange user id: ")

        db.session.add(a)
        db.session.commit()      

    if sel == 6:
        for s in Anonsers.query.all():
            print(f"{s.Id}  {s.Title}: {s.Description}")

    if sel == 7:
        b = Bud()

        for s in Users.query.all():
            print(f"{s.Id}  {s.Username}")
        b.User_Id = input ("Ange user id: ")       

        for s in Anonsers.query.all():
            print(f"{s.Id}  {s.Description}")
        selectedId = input("Ange your anons id:")
        b.Anonsers_Id = selectedId
        selected = Bud.query.filter_by(Anonsers_Id = selectedId)
        for row in selected:
            selected_first = Anonsers.query.filter_by(Id = selectedId).first()

        b.NewPrice = input("Ange a higher price:")

        db.session.add(b)
        db.session.commit()    
    