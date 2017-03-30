from flask import *
from flaskext.mysql import MySQL
import subprocess

app = Flask(__name__)

#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'demo'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'

#mysql = MySQL(app)


@app.route('/')

def home():
	if not session.get('logged_in'):

		return render_template('login.html')
	else:
		return "Successfully logged"


@app.route('/login',methods = ['POST'])


def login_name():

	username = request.form['username'] 
	password = request.form['password'] 

	sql_cmd = ["mysql", "-u","root", "-p","root", "-e","select * from demo.login_table where username = username and password = password"]
	
	results = subprocess.check_output(sql_cmd, shell=True)
       
        return results


if __name__ == "__main__":
	app.run(debug = True)
