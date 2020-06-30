from project import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    urole = db.Column(db.String(80))

    def __init__(self,username,password,urole):
        self.username = username
        self.password_hash = generate_password_hash(password=password)
        self.urole=urole

    def check_password(self,password):
        return check_password_hash(self.password_hash,password=password)


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.String(45), nullable=False, unique=True)
    name = db.Column(db.String(45), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bed_type = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(45), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    city = db.Column(db.String(45), nullable=False)
    state = db.Column(db.String(45), nullable=False)
    status = db.Column(db.String(45), nullable=False)


    def __init__(self,ssn_id, name, age, address, date, city, state, bed_type, status):
        self.ssn_id = ssn_id
        self.name = name
        self.age = age
        self.address = address
        self.date = date
        self.city = city
        self.state = state
        self.bed_type = bed_type
        self.status = status

class Medicines(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    mname = db.Column(db.String(20))
    mid = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    qissued = db.Column(db.Integer)
    children = db.relationship("MedicineMaster")
    def __init__(self,pid,mname,mid,rate,qissued):
        self.pid = pid
        self.mname = mname
        self.mid = mid
        self.rate  = rate
        self.qissued = qissued

class MedicineMaster(db.Model):
    __tablename__ = 'medicinemaster'
    mid = db.Column(db.Integer, ForeignKey('medicines.mid'), primary_key=True)
    mname = db.Column(db.String(20))
    qavailable = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    def __init__(self,mid,mname,qavailable,rate):
        self.mid = mid
        self.mname= mname
        self.qavailable = qavailable
        self.rate = rate


class Diagnostics(db.Model):
    __tablename__ = 'diagnostics'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    tname = db.Column(db.String(20))
    tid = db.Column(db.Integer)
    charge = db.Column(db.Integer)

    children = db.relationship("DiagnosticsMaster")
    def __init__(self,pid,tname,tid,charge):
        self.pid = pid
        self.tid = tid
        self.tname= tname
        self.charge = charge


class DiagnosticsMaster(db.Model):
    __tablename__ = 'diagnosticsmaster'
    tid = db.Column(db.Integer, ForeignKey('diagnostics.tid'), primary_key=True)
    tname = db.Column(db.String(20))
    tcharge = db.Column(db.Integer)
    def __init__(self,tid,tname,tcharge):
        self.tid = tid
        self.tname= tname
        self.tcharge = tcharge
