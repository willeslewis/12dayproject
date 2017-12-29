from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    multiply_text = text * 3
    return multiply_text

if __name__ == '__main__':
  app.run(port=33507)
