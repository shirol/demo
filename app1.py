from flask_wtf import *
from wtforms import *
from flask import *
from flask_admin.form import DatePickerWidget
from flaskext.mysql import MySQL
import csv
import xlsxwriter
import datetime
from time import mktime
import json
import flask.json

class MyEncoder(json.JSONEncoder):
        def default(self, obj):
                if isinstance(obj, datetime.datetime):
                        return int(mktime(obj.timetuple()))
                return json.JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = MyEncoder

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'demo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)

class GeneralForm(Form):
        start_date = DateField('start_date',widget=DatePickerWidget())
        end_date = DateField('end_date',widget=DatePickerWidget())
        submit = SubmitField('submit')

@app.route('/')

def home():
	return render_template('login.html')


@app.route('/login', methods = ['GET','POST'])

def login_name():
	username = request.form['username'] 
	password = request.form['password'] 
     
	cursor = mysql.get_db().cursor()    
	
	cursor.execute("select * from db1 where username='" + username + "' and password='" + password + "'")
	
	data = cursor.fetchall()
    		
	if data:
		return "Hi " +username+ " " +index()
	else:
		return 'Username or Password is wrong!!!'

	return home()


def home1():
        return render_template('date.html')


@app.route("/login1", methods = ['GET', 'POST'])

def index():
        form = GeneralForm(request.form)

        if request.method == 'POST':
        	start_date = form.start_date.data
                end_date = form.end_date.data

                if start_date < end_date:
             		#return "selected Start_date is " +str(start_date)+ " and selected End_date is " +str(end_date)
			return home2()
		else:
			return home1()

def home2():
	return render_template('wallet_input.html')


@app.route("/login2", methods = ['GET','POST'])

def index1():
	amount = request.form['amount']
	
	workbook = xlsxwriter.Workbook('output.xlsx')
        sheet = workbook.add_worksheet('transaction_details')

        cursor = mysql.get_db().cursor()

	try:
          cursor.execute("select * from demo_table where amount ='" + amount+ "'")

       	  data = cursor.fetchall()
          data1 = json.dumps(data, cls = MyEncoder)
	
	  for r, row in enumerate(data1):
	      for c, col in enumerate(row):
       		   sheet.write(r, c, col)

	except IndexError:
		print "error"

	return '<html> <body> Data copied to XLSX file <a href = "/downloadXLSX"> Click here to download. </a> </body> </html>'


@app.route("/downloadXLSX")

def getPlotExcel():
    	excelDownload = open("output.xlsx",'rb').read()
    
	return Response(
        	excelDownload,
        	mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        	headers = {"Content-disposition":
                 	   "attachment; filename=output.xlsx"})


if __name__ == "__main__":
	app.run(debug = True)
