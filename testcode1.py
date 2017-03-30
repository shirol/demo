from flask import Flask
from flaskext.mysql import *
from flask import Response
from flask import request
import json
import csv

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'demo'

mysql = MySQL(app)

@app.route('/')

def index1():
	cur = mysql.get_db().cursor()
	cur.execute('select * from wallet_table where wallet_id = 101')
	row = cur.fetchall()
	data = json.dumps(row)
	res = Response(data, status=200, mimetype='application/json')
	return res

@app.route('/id')

def index2():
	cur = mysql.get_db().cursor()
        cur.execute('select wallet_id from wallet_table')
        row = cur.fetchall()
	data = json.dumps(row)
	res = Response(data, status=200, mimetype='application/json')
        return res

@app.route('/name')

def index_2():
	cur = mysql.get_db().cursor()
	cur.execute('select name from wallet_table')
	row = cur.fetchall()
	data = json.dumps(row)
	res = Response(data, status=200, mimetype='application/json')
	return res

@app.route('/all')

def index_21():
	cur = mysql.get_db().cursor()
	cur.execute('select * from wallet_table')
	row = cur.fetchall()
	data = json.dumps(row)
	res = Response(data, status=200, mimetype='application/json')
	return res

@app.route('/product')

def index3():
        cur = mysql.get_db().cursor()
        cur.execute('select product from wallet_table')
        row = cur.fetchall()
	data = json.dumps(row)
        res = Response(data, status=200, mimetype='application/json')
	return res

if __name__ == '__main__':
        app.run(debug = True)
