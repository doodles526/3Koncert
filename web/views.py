from web import db, app, login_manager
from flask.ext.login import login_required, login_user, logout_user, current_user
from forms import *
from flask import request, redirect, url_for, render_template, g, session, flash
from web.models import User, Event, Event_Todo
from sqlalchemy import func

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

@login_required
@app.route("/logout")
def logout():
    logout_user()
    redirect(url_for('home'))

@app.route("/", methods=["GET", "POST"])
def landing():
    if current_user:
        redirect(url_for('home'))
    login_form = LoginForm(request.form)
    registration_form = CreateAccount(request.form)
    if login_form.validate_on_submit():
        user = User.query.filter_by(uName=login_form.name.data).first()
        if user.check_pass(login_form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Username/Password not recognized.")
            return redirect(url_for('landing'))

    if registration_form.validate_on_submit():
        new_user = User(registration_form.username.data,
                        registration_form.password.data,
                        registration_form.dob.data,
                        registration_form.fName.data,
                        registration_form.mName.data,
                        registration_form.lName.data,
                        int(registration_form.zip.data),
                        registration_form.email.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))
    return render_template('landing.html', login_form = login_form, reg = registration_form)


@login_required
@app.route('/home')
def home():
    #We use this query over the helper in this case because we don't 

    hot_events = db.session.query(Event, func.count(Event.attendees)).group_by(Event.id)
    return render_template('home.html', user_info=current_user, hot_events=hot_events)

@app.route('/create_event', methods=["GET", "POST"])
def create_event():
    form = CreateEvent(request.form)
    if form.validate():
        userid = g.db_connection("select UID from Users where uName = '%s'" % (session['user'])).first()[0]
        create_event(g.db_connection, form.name.data, form.zip.data, form.start_time.data, form.end_time.data, str(userid), form.external_link.data)
        print "success"
        flash("Event successfully created!")
        return redirect(url_for('event'))

    else:
        return render_template('create_event.html', form=form, user_info=current_user)


@app.route('/event/<event_id>')
def event(event_id):
    #might switch second INNER JOIN to OUTER
    get_event_sql = "SELECT e.eName AS eName, e.startTime AS startTime, e.endTime AS endTime, e.description AS description, uad.uName AS admin_name, uat.uName AS attend_name  FROM Events e INNER JOIN Event_Admin ead ON ead.EID = e.EID INNER JOIN Event_Attendees eat ON eat.EID = e.EID  INNER JOIN Users uat ON uat.UID = eat.UID INNER JOIN Users uad ON uad.UID = ead.UID WHERE e.EID = %d" % int(event_id)
   
    try: 
        event_info = g.db_connection.execute(get_event_sql).fetchall()
    except:    
        flash("Something happened and we weren't able to fetch this event. Sorry!")
        return redirect(url_for('events'))
    
    is_admin = False
    for user in event_info:
        if user['admin_name'] == session['user']:
            is_admin = True

    return render_template("event.html", event_info=event_info, is_admin=is_admin)

@app.route('/todo/<todo_id>')
def todo(todo_id):
    get_todo_sql= "SELECT et.name AS todo_name, et.description AS description, et.complete AS complete, u.uName AS uName, e.eName AS eName FROM Event_todo et INNER JOIN Event_assignment ea ON ea.todo_index = et.index INNER JOIN Users u ON ea.UID = u.UID INNER JOIN Events e ON e.EID = et.EID WHERE et.index = %d" % (todo_id)
    
    todo_info = g.db_connection.execute(get_todo_sql).fetchall()
    return render_template('todo.html', todo_info=todo_info)

@app.route('/create_todo/<event_id>', methods=['GOT', 'POST'])
def create_todo(event_id):
    form = CreateTodo()
    if form.validate():
        create_todo(g.db_connection(), event_id, form.title.data, form.description.data)
        return redirect("/event/%d" % (event_id))
    

#@app.route('/events')
#    get_events_sql = "SELECT e.eName, e.startTime,  FROM Events e INNER JOIN Users u ON u.UID = e.creatorID "


















