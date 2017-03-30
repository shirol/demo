from flask_wtf import *
from wtforms import *
from flask import *
from flask_admin.form import DatePickerWidget
from flaskext.mysql import MySQL
import csv
import xlsxwriter
from xlsxwriter.workbook import Workbook
import os
import datetime

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'demo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)


@app.route('/')
    
def home():
        return render_template('login.html')
	                
    
@app.route('/login', methods = ['GET','POST'])
    
def login_name():
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.get_db().cursor()

        cursor.execute("select * from login_table where username='" + username + "' and password='" + password + "'")

        data = cursor.fetchall()
	
        if data:
                return "<label>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Hi " +username+ "</label>" + date_input()
        else:
                error = "Invalid Username or Password!!!"
           	return render_template("login.html", error = error)

        return home()


def date_input():
        return render_template('date_input.html')


@app.route("/date", methods = ['GET', 'POST'])

def date_inputs():
        if request.method == 'POST':
              
		start_date1 = request.form['start_date']
		end_date1 = request.form['end_date']

		if start_date1 != "" and end_date1 != "":

			f = '%d/%m/%Y'
	
			start_date = datetime.datetime.strptime(start_date1, f)
			end_date = datetime.datetime.strptime(end_date1, f)

                	if start_date != "" and end_date != "" and start_date < end_date:
				error = ""                        			
                        	return checkbox_options(start_date,end_date,error)
			else:
				error = "Enter valid start date and end date"
                        	return render_template("date_input.html", error = error)

                else:
                        error = "Enter valid start date and end date"                        
			return render_template("date_input.html", error = error)
			
			
def checkbox_options(start_date,end_date,error):

        return render_template('checkbox_options.html', date = start_date, date1 = end_date, error = error)


@app.route("/no_options", methods = ['GET','POST'])

def no_options():
        start_date = request.form['date']
        end_date = request.form['date1']

        cursor = mysql.get_db().cursor()

        row_count = cursor.execute("select * from FactMasterB2B where SaleDate >= '" +start_date+ "' and SaleDate <= '" +end_date+"' limit 100")
	        
	if row_count > 1:

                row = cursor.fetchall()
		
                workbook = xlsxwriter.Workbook('output.xlsx')
                sheet = workbook.add_worksheet()
                for r, row1 in enumerate(row):
                        for c, col in enumerate(row1):
                                sheet.write(r, c, col)

                return '<html> <body> Data copied to XLSX file <a href = "/downloadXLSX"> Click here to download. </a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <a href="/logout"><b>Logout</b></a></body> </html>'

        else:
		error = ""
                return checkbox_options(start_date,end_date,error)


@app.route("/parameters", methods = ['GET','POST'])

def parameters():

	#TransID = request.form['TransID']
        #SaleDate = request.form['SaleDate']
        #SaleDateKey = request.form['SaleDateKey']
        MDN = request.form['MDN']
	TransactionNumber = request.form['TransactionNumber']
        WalletID = request.form['WalletID']

        start_date = request.form['date']
        end_date = request.form['date1']
	
        cursor = mysql.get_db().cursor()
	

	if request.form.get('WalletID_op') and request.form.get('MDN_op') and request.form.get('TransactionNumber_op'):

        	row_count = cursor.execute("select * from FactMasterB2B where WalletID = '" +WalletID + "' and MDN = '" +MDN +"' and TransactionNumber = '" +TransactionNumber+ "' and  SaleDate >= '" +start_date+"' and SaleDate <= '" +end_date+"'limit 100")


	elif request.form.get('WalletID_op') and request.form.get('MDN_op') and not request.form.get('TransactionNumber_op'):

                row_count = cursor.execute("select * from FactMasterB2B where WalletID = '" +WalletID + "' and MDN = '" +MDN +"' and  SaleDate >= '" +start_date+"' and SaleDate <= '" +end_date+"'limit 100")


	elif request.form.get('MDN_op') and request.form.get('TransactionNumber_op') and not request.form.get('WalletID_op'):

                row_count = cursor.execute("select * from FactMasterB2B where MDN = '" +MDN +"' and TransactionNumber = '" +TransactionNumber+ "' and  SaleDate >= '" +start_date+"' and SaleDate <= '" +end_date+"'limit 100")
	

	elif request.form.get('WalletID_op') and request.form.get('TransactionNumber_op') and not request.form.get('MDN_op'):

                row_count = cursor.execute("select * from FactMasterB2B where WalletID = '" +WalletID + "' and TransactionNumber = '" +TransactionNumber+ "' and  SaleDate >= '" +start_date+"' and SaleDate <= '" +end_date+"'limit 100")

	
	elif request.form.get('WalletID_op') and not request.form.get('MDN_op') and not request.form.get('TransactionNumber_op'):

		row_count = cursor.execute("select * from FactMasterB2B where WalletID = '" + WalletID + "' and SaleDate >= '" +start_date+"' and SaleDate <= '" +end_date+"'limit 100")
	
	
	elif request.form.get('MDN_op') and not request.form.get('WalletID_op') and not request.form.get('TransactionNumber_op'):

                row_count = cursor.execute("select * from FactMasterB2B where MDN = '" + MDN +"' and SaleDate >= '" +start_date+"' and SaleDate <= '" +end_date+"'limit 100")

        
	elif request.form.get('TransactionNumber_op') and not request.form.get('WalletID_op') and not request.form.get('MDN_op'):

                row_count = cursor.execute("select * from FactMasterB2B where TransactionNumber = '" + TransactionNumber +"' and SaleDate >= '" +start_date+"' and SaleDate <= '" +end_date+"'limit 100")

	
	else:
		error = "Please input information!!!!!"
		return checkbox_options(start_date, end_date, error)
	
	
	if row_count > 1:

                row = cursor.fetchall()
               
		workbook = xlsxwriter.Workbook('output.xlsx')
                sheet = workbook.add_worksheet()
                for r, row1 in enumerate(row):
                        for c, col in enumerate(row1):
                                sheet.write(r, c, col)

                return '<html> <body> Data copied to XLSX file <a href = "/downloadXLSX"> Click here to download. </a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <a href="/logout"><b>Logout</b></a></body> </html>'

        else:
		error="No transaction found!!!"
                return checkbox_options(start_date, end_date, error)
	

@app.route("/downloadXLSX")

def downloadExcel():
    excelDownload = open("output.xlsx",'rb').read()
    return Response(
        excelDownload,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-disposition":
                 "attachment; filename = output.xlsx"})


@app.route("/logout")

def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
#        app.secret_key = os.urandom(12)
        app.run(debug = True)
