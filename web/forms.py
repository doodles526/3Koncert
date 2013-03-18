from flask.ext.wtf import Form, DateField, DateTimeField, TextField, PasswordField, BooleanField, SelectField, SelectMultipleField, validators, Required, Email

class LoginForm(Form):
    name = TextField('Username/Email', [Required()])
    password = PasswordField('Password', [Required()])

class CreateAccount(Form):
    username = TextField("Username", [Required()])
    password = PasswordField("Password", [Required()])
    confirm_pass = PasswordField("Confirm Password", [Required()])
    email = TextField('Email', [Required()])
    fName = TextField('First Name', [Required()])
    mName = TextField('Middle Name/Initial')
    lName = TextField('Last Name', [Required()])
    zip = TextField('Zip code:(used for determining nearby events)', [Required()])
    dob = TextField('Date of Birth', [])

class CreateEvent(Form):
    name = TextField("Event Name", [Required()])
    zip = TextField("Zip Code", [Required()])
    description = TextField("Description")
    start_time = DateTimeField("Start Time", [Required()])
    end_time = DateTimeField("End Time")
    external_link = TextField("External Link")

class CreateTodo(Form):
    title = TextField("Title", [Required()])
    description = TextField("Description")

class AssignTodo(Form):
    username = TextField('User', [Required()])

