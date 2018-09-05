import os
from   flask import Flask, render_template, request, redirect, Response
from   bokeh.embed import components

# For stock ticker stuff
import pandas as pd
from   bokeh.plotting import figure, output_file, show
import quandl
my_api_key = 'L2BgXpq4eVihjReXAR64'
quandl.ApiConfig.api_key = my_api_key


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/make_plot', methods=['POST'])
def make_plot():
  stock = request.form['stock']
  year = request.form['year']
  month = request.form['month']
  p = plot_stock(stock=stock, year=year, month=month)
  if isinstance(p, str):
    # returned error message instead of a plot
    return p
  else:
    script, div = components(p)
    return render_template('bokeh_plot.html', script=script, div=div)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/stocks')
def stocks():
  with open('static/WIKI-datasets-codes-sorted.csv', 'r') as f:
    #content = f.read()
    return Response(f.read(), mimetype='text/plain')


"""
Stock ticker functionality is below. I'd prefer to make this as a separate module, but this requires instructing Flask how to find it, which seems nontrivial and prone to breaking when ported over to Heroku.
"""

test_stock = 'AAPL'
test_year = '2017'
test_month = '09'

month_dictionary = {'JANUARY':'01', 'FEBRUARY':'02', 'MARCH':'03', 'APRIL':'04',
                    'MAY':'05', 'JUNE':'06', 'JULY':'07', 'AUGUST':'08', 'SEPTEMBER':'09',
                    'OCTOBER':'10', 'NOVEMBER':'11', 'DECEMBER':'12',
                    'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04',
                    'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09',
                    'OCT':'10', 'NOV':'11', 'DEC':'12'}

def plot_stock(stock=test_stock, year=test_year, month=test_month):

    stock = stock.upper()
    
    # Check for valid year formatting
    year = str(year)
    if len(year) != 4:
        return "PLEASE ENTER A VALID 4-DIGIT YEAR!!"
    
    # If needed, transform the month into the 2-digit form
    month = str(month).upper()
    if month in month_dictionary:
        month = month_dictionary[month]
    if month.isdigit() and int(month) >= 1 and int(month) <= 12:
        month = str(int(month)).zfill(2)
    else:
        return "UNKNOWN MONTH!!"
        
    # Request the data
    mydata = pd.DataFrame()
    try:
        # just grab the data for an entire year...
        # month requests are fragile (e.g. Feb 29 often breaks it!)
        mydata = quandl.get('WIKI/'+stock, start_date=year+'-01-01', end_date=year+'-12-31')
    except:
        # ** consider linking to a website that shows a list a valid stocks
        return "COULDN'T FIND THAT STOCK!"
    
    # Extract closing prices for the desired month
    close_prices = pd.Series()
    try:
        if month=='12':
          close_prices = mydata['Close'].loc[(mydata.index >= year+'-'+month)]
        else:
          close_prices = mydata['Close'].loc[(mydata.index >= year+'-'+month) &
                                             (mydata.index <  year+'-'+str(int(month)+1))]
    except:
        return "COULDN'T FIND DATA IN THAT TIME PERIOD"
    
    p = figure(title=stock + '  (' + year + '-' + month + ')', x_axis_label='Day in ' + year + '-' + month, y_axis_label='Closing Price (USD)')
    p.title.text_font_size = '20pt'
    p.xaxis.axis_label_text_font_size = '14pt'
    p.xaxis.major_label_text_font_size = '12pt'
    p.yaxis.axis_label_text_font_size = '14pt'
    p.yaxis.major_label_text_font_size = '12pt'
    x = pd.DatetimeIndex(close_prices.index.values).day
    y = close_prices.values
    #p.line(x, y, legend="Temp.", line_width=2)
    p.line(x, y, line_width=3)
    return p


if __name__ == '__main__':
  #app.run(port=33507)
  # I'm not sure if the below modifications are even necessary...
  port = int(os.environ.get("PORT", 33507))
  app.run(host='0.0.0.0', port=port)
