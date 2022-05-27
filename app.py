from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL
import mysql.connector
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = '3307' 
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'lab45db'
app.config['SECRET_KEY'] = 'super secret key alabama sweet'

mysql = MySQL(app)


# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


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

app.run(host='localhost', port=5000, debug=True)





