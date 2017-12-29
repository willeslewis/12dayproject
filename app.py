from plots import build_plot
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/')
def render_plot():
    plot_snippet = build_plot()
    
    return render_template('plots.html', snippet=plot_snippet)

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    multiply_text = text * 3
    return multiply_text

if __name__ == '__main__':
  app.run(port=33507)
