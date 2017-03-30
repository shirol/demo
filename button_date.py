from flask_wtf import *
from wtforms import *
from flask import *
from flask_admin.form import DatePickerWidget

app = Flask(__name__)

class GeneralForm(Form):
	start_date = DateField('start_date',widget=DatePickerWidget())
	end_date = DateField('end_date',widget=DatePickerWidget())
	submit = SubmitField('submit')

@app.route("/")

def home():
	return render_template('date.html')

@app.route("/login1", methods=['GET', 'POST'])

def index():
	form = GeneralForm(request.form)
	
	if request.method == 'POST':
		start_date = form.start_date.data
       		end_date = form.end_date.data
		
		return "selected Start_date is " +str(start_date)+ " and selected End_date is " +str(end_date)			
	else:
		return home()

if __name__ == '__main__':
	app.run(debug=True)
