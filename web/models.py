from web import db, login_manager
import datetime
from werkzeug.security import generate_password_hash, check_password_hash



todo_assignment = db.Table("event_todo_assignment", db.Model.metadata,
    db.Column('todo_index', db.Integer(), db.ForeignKey('event_todo.index')),
    db.Column('uid', db.Integer(), db.ForeignKey('users.id'))
)

event_admin = db.Table('event_admin', db.Model.metadata,
    db.Column('uid', db.Integer(), db.ForeignKey("users.id")),
    db.Column('eid', db.Integer(), db.ForeignKey("events.id"))
)

event_attendees = db.Table('event_attendees', db.Model.metadata,
    db.Column('uid', db.Integer(), db.ForeignKey('users.id')),
    db.Column('eid', db.Integer(), db.ForeignKey('events.id'))
)


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer(), primary_key=True)
    eName = db.Column(db.String(255), nullable = False)
    zip = db.Column(db.Integer())
    startTime = db.Column(db.DateTime(), nullable = False)
    endTime = db.Column(db.DateTime())
    description = db.Column(db.Text())
    creatorID = db.Column(db.Integer(), db.ForeignKey('users.id'))
    externalLink = db.Column(db.String(255))
    admins = db.relationship("User", secondary=event_admin, backref=db.backref("admin_of", lazy='dynamic'), lazy='dynamic')
    attendees = db.relationship("User", secondary=event_attendees, backref=db.backref('attending', lazy='dynamic'), lazy='dynamic')
    
    def __init__(self, eName, zip, startTime, endTime, description, creatorID, externalLink = None):
        self.eName = eName
        self.zip = zip
        self.startTime = startTime
        self.endTime = endTime
        self.description = description
        self.creatorID = creatorID
        self.externalLink = externalLink

class Event_Todo(db.Model):
    __tablename__ = "event_todo"
    index = db.Column(db.Integer(), primary_key = True)
    id = db.Column(db.Integer(), db.ForeignKey('events.id'))
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text())
    complete = db.Column(db.Boolean())
    assigned_to = db.relationship("User", secondary=todo_assignment, backref=db.backref('todos', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.complete = False

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key = True)
    uName = db.Column(db.String(16), nullable = False)
    pWord = db.Column(db.String(255), nullable = False)
    dateBirth = db.Column(db.Date(), nullable = False)
    fName = db.Column(db.String(50), nullable = False)
    mName = db.Column(db.String(50))
    lName = db.Column(db.String(50), nullable = False)
    zip = db.Column(db.Integer(), nullable = False)
    eMail = db.Column(db.String(60), nullable = False)
    createDate = db.Column(db.DateTime(), nullable = False)

    def __init__(self, uName, pWord, dateBirth, fName, mName, lName, zip, eMail):
        self.uName = uName 
        self.pWord = generate_password_hash(pWord)
        self.dateBirth = dateBirth
        self.fName = fName
        self.mName = mName
        self.lName = lName
        self.zip = zip
        self.eMail = eMail
        self.createDate = datetime.datetime.now()

    def check_pass(self, clear_pass):
        return check_password_hash(self.pWord, clear_pass)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

