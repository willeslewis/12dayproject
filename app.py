#import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components 
import pandas as pd
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

uservars={}

def datetime(x):
  return np.array(x,dtype=np.datetime64)


def stock_load(ticker_name):

  api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % stock
  r=requests.get(api_url)
  myjson=r.json()
  tickerdata=pd.DataFrame(myjson['dataset']['data'],columns=['Date','Open','High','Low','Close','Volume','Ex-Dividend','Split Ratio','Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume'])

  return tickerdata

def create_plot(tickerdata,ticker_name):
  
  p1 =figure(x_axis_type="datetime",title="Stock Prices")

  p1.grid.grid_line_alpha=0.3

  p1.xaxis.axis_label='Date'

  p1.yaxis.axis_label='Price'

  p1.line(datetime(tickerdata['Date']),tickerdata['Adj. Close'],color='red',legend='AAPL')

  p1.legend.location='top_left'

@app.route('/')
def main():
  return redirect('/index')


# Index page
@app.route('/index',methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/plot.html',methods=['POST'])
def create_plot():

  uservars['ticker']=request.form['ticker']

  tickerdata=stock_load(request.form['ticker'])
  
  p1 =figure(x_axis_type="datetime",title="Stock Prices")

  p1.grid.grid_line_alpha=0.3

  p1.xaxis.axis_label='Date'

  p1.yaxis.axis_label='Price'

  if request.form.get('Close'):
    p1.line(datetime(tickerdata['Date']),tickerdata['Close'],color='red',legend='AAPL')
  if request.form.get('Open'):
    p1.line(datetime(tickerdata['Date']),tickerdata['Open'],color='red',legend='AAPL')
  if request.form.get('Adj. Close'):
    p1.line(datetime(tickerdata['Date']),tickerdata['Adj. Close'],color='red',legend='AAPL')
  if request.form.get('Adj. Open'):
    p1.line(datetime(tickerdata['Date']),tickerdata['Adj. Open'],color='red',legend='AAPL')
  p1.legend.location='top_left'

  script, div = components(p)

  return render_template('plot.html',script=script,div=div)


if __name__ == '__main__':
  app.run(host='0.0.0.0',port=33507)
