from flask import Flask, render_template, request

import plotly
import plotly.graph_objs as go
import pandas as pd
import json
from sqlalchemy import create_engine

import imblearn
import joblib

lendclub = pd.read_csv("./static/lendingclub.csv")
app = Flask(__name__)


##################################################
def category_plot(
    cat_plot = 'histplot',
    cat_x = 'loan_status', cat_y = 'int_rate',
    estimator = 'count', hue = 'loan_status'):

    # generate dataframe tips.csv
    # tips = pd.read_csv('./static/tips.csv')

    # jika menu yang dipilih adalah histogram
    if cat_plot == 'histplot':
        # siapkan list kosong untuk menampung konfigurasi hist
        data = []
        # generate config histogram dengan mengatur sumbu x dan sumbu y
        for val in lendclub[hue].unique():
            hist = go.Histogram(
                x=lendclub[lendclub[hue]==val][cat_x],
                y=lendclub[lendclub[hue]==val][cat_y],
                histfunc=estimator,
                name=val
            )
            #masukkan ke dalam array
            data.append(hist)
        #tentukan title dari plot yang akan ditampilkan
        title='Count Plot'
    elif cat_plot == 'boxplot':
        data = []

        for val in lendclub[hue].unique():
            box = go.Box(
                x=lendclub[lendclub[hue] == val][cat_x], #series
                y=lendclub[lendclub[hue] == val][cat_y],
                name = val
            )
            data.append(box)
        title='Box'
    # menyiapkan config layout tempat plot akan ditampilkan
    # menentukan nama sumbu x dan sumbu y
    if cat_plot == 'histplot':
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title='person'),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    else:
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=cat_y),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    #simpan config plot dan layout pada dictionary
    result = {'data': data, 'layout': layout}

    #json.dumps akan mengenerate plot dan menyimpan hasilnya pada graphjson
    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
##################################################

#1 HOME/INDEX
@app.route('/')
def index():
	plot = category_plot()
    # dropdown menu
    # kita lihat pada halaman dashboard terdapat menu dropdown
    # terdapat lima menu dropdown, sehingga kita mengirimkan kelima variable di bawah ini
    # kita mengirimnya dalam bentuk list agar mudah mengolahnya di halaman html menggunakan looping
	list_plot = [('histplot', 'Count Plot'), ('boxplot', 'Box Plot')]
	list_x = [('loan_status', 'Loan Status'), ('purpose', 'Purpose'), ('grade', 'Grade'), ('sub_grade', 'Sub Grade'), ('term', 'Loan Term'), ('emp_length', 'Employment Length'), ('home_ownership', 'Home Ownership'), ('initial_list_status', 'Initial List Status'), ('application_type', 'Application Type')]
	list_y = [('int_rate', 'Interest Rate'), ('loan_amnt', 'Loan Amount'), ('installment', 'Installment'), ('annual_inc', 'Annual Income'), ('dti', 'Debt-to-Income Ratio'), ('pub_rec', 'Derogatory Public Record'), ('revol_bal', 'Revolving Balance'), ('mort_acc', 'Mortgage Account'), ('pub_rec_bankruptcies', 'Public Record of Bankruptcies')]
	list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
	list_hue = [('loan_status', 'Loan Status'), ('purpose', 'Purpose'), ('grade', 'Grade'), ('sub_grade', 'Sub Grade'), ('term', 'Loan Term'), ('emp_length', 'Employment Length'), ('home_ownership', 'Home Ownership'), ('initial_list_status', 'Initial List Status'), ('application_type', 'Application Type')]

	return render_template('category.html', plot = plot, focus_plot = 'histplot', focus_x = 'loan_status', focus_estimator = 'count', focus_hue = 'loan_status', drop_plot = list_plot, drop_x = list_x, drop_y = list_y, drop_estimator = list_est, drop_hue = list_hue)
		
	'''
		# file yang akan menjadi response dari API
		'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot='histplot',
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x='grade',

        # untuk sumbu Y tidak ada, nantinya menu dropdown Y akan di disable
        # karena pada histogram, sumbu Y akan menunjukkan kuantitas data

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator='count',
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue='loan_status',
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_est,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue)
		
	'''

# ada dua kondisi di mana kita akan melakukan request terhadap route ini
# pertama saat klik menu tab (Histogram & Box)
# kedua saat mengirim form (saat merubah salah satu dropdown) 

# 2) VISUALISASI
@app.route('/cat_fn/<nav>')
def cat_fn(nav):

    # saat klik menu navigasi
    if nav == 'True':
        cat_plot = 'histplot'
        cat_x = 'grade'
        cat_y = 'int_rate'
        estimator = 'count'
        hue = 'loan_status'
    
    # saat memilih value dari form
    else:
        cat_plot = request.args.get('cat_plot')
        cat_x = request.args.get('cat_x')
        cat_y = request.args.get('cat_y')
        estimator = request.args.get('estimator')
        hue = request.args.get('hue')

    # Dari boxplot ke histogram akan None
    if estimator == None:
        estimator = 'count'
    
    # Saat estimator == 'count', dropdown menu sumbu Y menjadi disabled dan memberikan nilai None
    if cat_y == None:
        cat_y = 'int_rate'

    # Dropdown menu
    list_plot = [('histplot', 'Count Plot'), ('boxplot', 'Box Plot')]
    list_x = [('loan_status', 'Loan Status'), ('purpose', 'Purpose'), ('grade', 'Grade'), ('sub_grade', 'Sub Grade'), ('term', 'Loan Term'), ('emp_length', 'Employment Length'), ('home_ownership', 'Home Ownership'), ('initial_list_status', 'Initial List Status'), ('application_type', 'Application Type')]
    list_y = [('int_rate', 'Interest Rate'), ('loan_amnt', 'Loan Amount'), ('installment', 'Installment'), ('annual_inc', 'Annual Income'), ('dti', 'Debt-to-Income Ratio'), ('pub_rec', 'Derogatory Public Record'), ('revol_bal', 'Revolving Balance'), ('mort_acc', 'Mortgage Account'), ('pub_rec_bankruptcies', 'Public Record of Bankruptcies')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('loan_status', 'Loan Status'), ('purpose', 'Purpose'), ('grade', 'Grade'), ('sub_grade', 'Sub Grade'), ('term', 'Loan Term'), ('emp_length', 'Employment Length'), ('home_ownership', 'Home Ownership'), ('initial_list_status', 'Initial List Status'), ('application_type', 'Application Type')]

    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
	
    return render_template('category.html',plot=plot,focus_plot='histplot',focus_x='loan_status',focus_estimator='count',focus_hue='loan_status',drop_plot=list_plot,drop_x=list_x,drop_y=list_y,drop_estimator=list_est,drop_hue=list_hue)
	

#3 DATASET + PREDICTING
@app.route('/invest')
def invest():
	lendclub = pd.read_csv("./static/lendingclub.csv").head(100)
	lendclub.index.name = None
	titles = " "
	
	# data.to_html()
	return render_template('invest.html', tables = [lendclub.to_html(classes = 'data', header = 'true')], titles = titles)

#4 RESULT
@app.route('/result', methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		input = request.form

		loan_amnt = float(input['loan_amnt'])
		term = input['term']
		int_rate = float(input['int_rate'])
		installment = float(input['installment'])
		grade = input['grade']
		sub_grade = input['sub_grade']
		emp_length = input['emp_length']
		home_ownership = input['home_ownership']
		annual_inc = float(input['annual_inc'])
		verification_status = input['verification_status']
		issue_d = input['issue_d']
		purpose = input['purpose']
		dti = float(input['dti'])
		earliest_cr_line = input['earliest_cr_line']
		open_acc = float(input['open_acc'])
		pub_rec = float(input['pub_rec'])
		revol_bal = float(input['revol_bal'])
		revol_util = float(input['revol_util'])
		total_acc = float(input['total_acc'])
		initial_list_status = input['initial_list_status']
		application_type = input['application_type']
		mort_acc = float(input['mort_acc'])
		pub_rec_bankruptcies = float(input['pub_rec_bankruptcies'])
		address = input['address']

		data_pred = pd.DataFrame(data =[[loan_amnt, term, int_rate, installment, grade, sub_grade, emp_length, home_ownership, annual_inc, verification_status, issue_d, purpose, dti, earliest_cr_line, open_acc, pub_rec, revol_bal, revol_util, total_acc, initial_list_status, application_type, mort_acc, pub_rec_bankruptcies, address]], 
								columns = ['loan_amnt', 'term', 'int_rate', 'installment', 'grade', 'sub_grade','emp_length', 'home_ownership', 'annual_inc', 'verification_status','issue_d', 'purpose', 'dti', 'earliest_cr_line', 'open_acc', 'pub_rec','revol_bal', 'revol_util', 'total_acc', 'initial_list_status','application_type', 'mort_acc', 'pub_rec_bankruptcies', 'address']
								)

		## Predicting
		model = joblib.load('lc_piperf')

		pred = model.predict(data_pred)[0]
		proba = model.predict_proba(data_pred)

		if pred == 0:
			pred = "Charged Off"
			proba = f"{round(proba[0][0]*100, 2)}%"
		else:
			pred =  "Fully Paid"
			proba = f"{round(proba[0][1]*100, 2)}%"


		return render_template('result.html', 
								loan_amnt = loan_amnt,
								term = term,
								int_rate = int_rate,
								installment = installment,
								grade = grade,
								sub_grade = sub_grade,
								# emp_title = input['emp_title'],
								emp_length = emp_length,
								home_ownership = home_ownership,
								annual_inc = annual_inc,
								verification_status = verification_status,
								issue_d = issue_d,
								purpose = purpose,
								dti = dti,
								earliest_cr_line = earliest_cr_line,
								open_acc = open_acc,
								pub_rec = pub_rec,
								revol_bal = revol_bal,
								revol_util = revol_util,
								total_acc = total_acc,
								initial_list_status = initial_list_status,
								application_type = application_type,
								mort_acc = mort_acc,
								pub_rec_bankruptcies = pub_rec_bankruptcies,
								address = address,
								pred_borrowers = pred, 
								proba_borrowers = proba
								)










if __name__ == '__main__':
	model = joblib.load('lc_tunedrf')
	app.run(debug = True)