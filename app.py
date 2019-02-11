import os
from   flask import Flask, render_template, request, redirect, Response
from   bokeh.embed import components

import plot_stock_module

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/make_plot', methods=['POST'])
def make_plot():
  stock = request.form['stock']
  year = request.form['year']
  month = request.form['month']
  p = plot_stock_module.plot_stock(stock=stock, year=year, month=month)
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


if __name__ == '__main__':
  #app.run(port=33507)
  # I'm not sure if the below modifications are necessary, but just in case
  port = int(os.environ.get("PORT", 33507))
  app.run(host='0.0.0.0', port=port)
