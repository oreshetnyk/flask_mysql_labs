from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Add Secret Key
app.config['SECRET_KEY'] = 'super secret sweet key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize The Database
db = SQLAlchemy(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def _init__(self, name, email):
        self.name = name
        self.email = email
    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


#db.create_all()
#db.session.commit()


# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Add User
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form')
def form():
    return render_template('form.html')


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error 
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template('name.html', name = name, form = form)





'''
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return 'Login via the login Form'

    if request.method == 'POST':
        id = int(request.form['id'])
        name = request.form['name']
        position = request.form['position']
        #cabinet = int(request.form['cabinet'])
        #service = request.form['service']
        #salary = int(request.form['salary'])
        #contract_number = int(request.form['contract_number'])
        print(name, type(name))
        print(position, type(position))
        #print(cabinet, type(cabinet)) 
        #print(time, type(time))
        #print(service, type(service))
        #print(salary, type(salary))
        #print(contract_number, type(contract_number))
        query = 'INSERT INTO doctors (id, name, position) VALUES(%s, "%s", "%s");' % (id, name, position)
        cursor = mysql.connection.cursor()
        print(query)
        
        cursor.execute(query)

        mysql.connection.commit()

        cursor.close()
        return f'Done!'
'''


app.run(host='localhost', port=5000, debug=True)





