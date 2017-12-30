import requests
from bokeh.plotting import figure
from bokeh.embed import components 
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

uservars={}

#def stock_load(ticker_name):

#  api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % stock
#  r=requests.get(api_url)
#  myjson=r.json()
#  tickerdata=pd.DataFrame(myjson['dataset']['data'],columns=['Date','Open','High','Low','Close','Volume','Ex-Dividend','Split Ratio','Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume'])

#  return tickerdata

@app.route('/')
def main():
  return redirect('/index')


# Index page
@app.route('/index',methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/plot',methods=['POST'])
def plot():

  uservars['ticker']=request.form['ticker']
  api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % uservars['ticker']
  r=requests.get(api_url)
  myjson=r.json()
  tickerdata=pd.DataFrame(myjson['dataset']['data'],columns=['Date','Open','High','Low','Close','Volume','Ex-Dividend','Split Ratio','Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume'])  
  d = datetime.now() - timedelta(days=365)
	
  #tickerdata=tickerdata[pd.to_datetime(tickerdata['Date'])>=d]
  p1 =figure(x_axis_type="datetime",title="Stock Prices for %s" %uservars['ticker'], x_range(d,datetime.now()))

  p1.xaxis.axis_label='Date'

  p1.yaxis.axis_label='Price'

  if request.form.get('Close'):
    p1.line(pd.to_datetime(tickerdata['Date']),tickerdata['Close'],color='red',legend='Close')
  if request.form.get('Open'):
    p1.line(pd.to_datetime(tickerdata['Date']),tickerdata['Open'],color='green',legend='Open')
  if request.form.get('Adj. Close'):
    p1.line(pd.to_datetime(tickerdata['Date']),tickerdata['Adj. Close'],color='orange',legend='Adj. Close')
  if request.form.get('Adj. Open'):
    p1.line(pd.to_datetime(tickerdata['Date']),tickerdata['Adj. Open'],color='blue',legend='Adj. Open')
  p1.legend.location='top_left'

  script, div = components(p1)

  return render_template('plot.html',script=script,div=div)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=33507)  
