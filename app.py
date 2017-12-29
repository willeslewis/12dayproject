import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components 
from bokeh.charts import Histogram
import pandas as pd
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Load the Iris Data Set
iris_df = pd.read_csv("data/iris.data", 
    names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
feature_names = iris_df.columns[0:-1].values.tolist()

# Create the main plot
def create_figure(current_feature_name, bins):
	p = Histogram(iris_df, current_feature_name, title=current_feature_name, color='Species', 
	 	bins=bins, legend='top_right', width=600, height=400)

	# Set the x axis label
	p.xaxis.axis_label = current_feature_name

	# Set the y axis label
	p.yaxis.axis_label = 'Count'
	return p


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

# Index page
@app.route('/')
def index():
	# Determine the selected feature
	current_feature_name = request.args.get("feature_name")
	if current_feature_name == None:
		current_feature_name = "Sepal Length"

	# Create the plot
	plot = create_figure(current_feature_name, 10)
		
	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("iris_index1.html", script=script, div=div,
		feature_names=feature_names,  current_feature_name=current_feature_name)


#@app.route('/')
#def index():

  #stock='AAPL'
  #api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % stock

  #r=requests.get(api_url)
  #myjson=r.json()

  #tickerdata=pd.DataFrame(myjson['dataset']['data'],columns=['Date','Open','High','Low','Close','Volume','Ex-Dividend','Split Ratio','Adj. Open','Adj. High','Adj. Low','Adj. Close','Adj. Volume'])

  #def datetime(x):
        
  #  return np.array(x,dtype=np.datetime64)

  #p1 =figure(x_axis_type="datetime",title="Stock Prices")

  #p1.grid.grid_line_alpha=0.3

  #p1.xaxis.axis_label='Date'

  #p1.yaxis.axis_label='Price'

  #p1.line(datetime(tickerdata['Date']),tickerdata['Adj. Close'],color='#A6CEE3',legend='AAPL')

  #p1.line(datetime(tickerdata['Date']),tickerdata['Adj. Open'],color='red',legend='AAPL')

  #p1.legend.location='top_left'

  #script, div = components(p1)

#  return render_template('index.html')

if __name__ == '__main__':
  app.run(port=33507)
