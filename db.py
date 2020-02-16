from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PhoneNumberType

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    about = db.Column(db.String)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)    
    price = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.JSON)
    free = db.Column(db.JSON, nullable=False)
    bookings = db.relationship("Booking", back_populates="teacher")


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(PhoneNumberType(), nullable=False)
    day = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    teacher = db.relationship("Teacher", back_populates="bookings")
    teacher_id = db.Column(db.String, db.ForeignKey("teachers.id"))


class Study_Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String)
    time = db.Column(db.String(70))
    name = db.Column(db.String, nullable=False)
    phone = db.Column(PhoneNumberType(), nullable=False)


db.create_all()
