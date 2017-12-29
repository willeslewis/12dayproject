import numpy as np
from bokeh.plotting import figure,show,output_notebook
from bokeh.embed import components 
import pandas as pd
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():

  stock='AAPL'
  api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % stock

  r=requests.get(api_url)
  myjson=r.json()

  tickerdata=pd.DataFrame(myjson['dataset']['data'],columns=['Date','Open','High','Low','Close','Volume','Ex-Dividend','Split Ratio','Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume'])

  def datetime(x):
        
    return np.array(x,dtype=np.datetime64)

  p1 =figure(x_axis_type="datetime",title="Stock Prices")

  p1.grid.grid_line_alpha=0.3

  p1.xaxis.axis_label='Date'

  p1.yaxis.axis_label='Price'

  p1.line(datetime(tickerdata['Date']),tickerdata['Adj. Close'],color='#A6CEE3',legend='AAPL')

  p1.line(datetime(tickerdata['Date']),tickerdata['Adj. Open'],color='red',legend='AAPL')

  p1.legend.location='top_left'

  script, div = components(p1)

  return render_template('index.html',script=script,div=div)

if __name__ == '__main__':
  app.run(port=33507)
