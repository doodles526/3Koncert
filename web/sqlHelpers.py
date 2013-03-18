from werkzeug.security import check_password_hash, generate_password_hash
import datetime

def verify_user(db, uName, pWord):
    try:
        hashed_pw = db.execute('select pWord from Users where uName = "%s"' % (uName)).first()[0]
        
    except:
        print "sql error"
        return False

    return check_password_hash(hashed_pw, pWord)

def create_account(db, uName, pWord, email, fName, mName, lName, zip, dob):
    db.execute("INSERT into Users  (uName, pWord, eMail, fName, mName, lName, zip, createDate)   VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % (uName, generate_password_hash(pWord), email, fName, mName, lName, str(zip), str(datetime.datetime.now()).split('.')[0]))

def create_event(db, eName, zip, startTime, endTime, description, creatorID, externalLink):
    #create the Event instance
    eventid = db.execute("INSERT INTO Events (eName, zip, startTime, endTime, description, creatorID, externalLink) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (eName, str(zip), str(startTime), str(endTime), description, str(creatorID), externalLink)).lastrowid
    
    db.execute("INSERT INTO Event_Admin (UID, EID) VALUES ('%s', '%s')" % (creatorID, eventid))
    db.execute("INSERT INTO Event_Attendees (UID, EID) VALUES ('%s', '%s')" % (creatorID, eventid))

def get_user_info(db, uName):
    return db.execute("SELECT uName, fName, mName, lName, zip FROM Users where uName = '%s'" % (uName)).first()

def get_hot_events(db, num_events, zip):
    return db.execute("SELECT e.uName, e.zip, e.startTime, e.endTime, e.description, e.creatorID, e.externalLink, count(et.EID) FROM Events e INNER JOIN Event_Attendees et on Events.EID = EventAttendees.EID where e.zip = '%s' ORDER BY count(et.EID) DESC LIMIT '%s'" % (zip, str(num_events))).fetchall()


def create_todo(db, event_id, name, description):
    db.execute("INSERT INTO Event_todo (EID, name, description, complete) VALUES (%d, %s, %s, 0)" % (event_id, name, description))












