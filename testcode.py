from flask import *
from flaskext.mysql import MySQL
import json
import datetime
from time import mktime
import flask.json
import decimal

class MyEncoder(json.JSONEncoder):
	def default(self, obj):
        	if isinstance(obj, datetime.datetime):
            		return int(mktime(obj.timetuple()))
       	 	return json.JSONEncoder.default(self, obj)

class MyJSONEncoder(flask.json.JSONEncoder):
	def default(self, obj):
        	if isinstance(obj, decimal.Decimal):
            		return str(obj)
        	return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.json_encoder = MyEncoder

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/api_Fact_oxiwalleT')

def index():
        cur = mysql.get_db().cursor()
        cur.execute('select * from fact_oxiwallet limit 10')
        row = cur.fetchall()
	data = json.dumps(row, cls = MyJSONEncoder)
	res = Response(data, status = 200, mimetype = 'application/json')
	return data                                                     

@app.route('/api_Fact_oxiwallet_categorY')

def index1():
        cur = mysql.get_db().cursor()
        cur.execute('select * from fact_oxiwallet_category')
        row = cur.fetchall()
	data = json.dumps(row)
	res = Response(data, status = 200, mimetype = 'application/json')
        return data

@app.route('/api_Fact_oxiwallet_producT')

def index2():
	cur = mysql.get_db().cursor()
	cur.execute('select * from fact_oxiwallet_product')
	row = cur.fetchall()
	data = json.dumps(row)
	res = Response(data, status = 200, mimetype = 'application/json')
	return data

@app.route('/api_Fact_oxiwallet_subcategorY')

def index3():
	cur = mysql.get_db().cursor()
	cur.execute('select * from fact_oxiwallet_subcategory')
	row = cur.fetchall()
	data = json.dumps(row)
	res = Response(data, status = 200, mimetype = 'application/json')
	return data

@app.route('/api_Fact_oxiwallet_totaL')

def index4():
	cur = mysql.get_db().cursor()
	cur.execute('select * from fact_oxiwallet_total')
	row = cur.fetchall()
	data = json.dumps(row)
	res = Response(data, status = 200, mimetype = 'application/json')
	return data

@app.route('/api_Oxiwallet_transaction_historY')

def index5():
        cur = mysql.get_db().cursor()
        cur.execute('select * from oxiwallet_transaction_history limit 10')
        row = cur.fetchall()
	data = json.dumps(row, cls = MyEncoder)
        res = Response(data, status = 200, mimetype = 'application/json')
        return data

if __name__ == '__main__':
        app.run(debug = True)
