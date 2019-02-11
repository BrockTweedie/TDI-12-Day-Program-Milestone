import os
import pandas as pd
from   bokeh.plotting import figure, output_file, show
import quandl
quandl.ApiConfig.api_key = str(os.getenv('QUANDL_API_KEY'))


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
    if len(year) != 4 or not year.isdigit():
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
      return f"COULDN'T FIND STOCK {stock}!"
    
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
    p.line(pd.DatetimeIndex(close_prices.index.values).day,
           close_prices.values,
           line_width=3)
    return p


## Execute only if run as a script
if __name__ == "__main__":
    main()
