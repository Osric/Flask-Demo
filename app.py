import requests
import simplejson
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.vars = {}

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        app.vars['ticker'] = request.form['ticker']
        app.vars['features'] = request.form.getlist('features')
        return redirect('/graph')

@app.route('/error-quandle')
def error():
    details = "Most likely, the ticker you entered was not found in the dataset."
    return render_template('error.html', culprit='Quandle', details=details)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
