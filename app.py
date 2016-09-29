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

@app.route('/graph')
def graph():
    stock = app.vars['ticker'].upper()
    features = [feature for feature in app.vars['features']]
    
    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)
    json_data = simplejson.loads(raw_data.content)
    
    if len(json_data) == 1:
        return redirect('/error-quandle')
    
    df = pd.DataFrame(json_data['data'], columns=json_data['column_names'])
    df.set_index(pd.DatetimeIndex(df['Date']), inplace=True)
    
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"
    
    plot = figure(tools=TOOLS, 
                  title="Data from Quandle WIKI set", 
                  x_axis_label="date", x_axis_type="datetime")
    
    colors = ['blue', 'green', 'orange', 'red']
    repeats = len(features) / len(colors)
    colorwheel = colors * (1 + repeats)
    index = 0
    
    for feature in features:
        plot.line(df[feature].index, df[feature], line_color=colorwheel[index],legend=stock+': '+feature)
        index += 1
        
        script, div = components(plot)
        return render_template('graph.html', script=script, div=div, stock=stock)

@app.route('/error-quandle')
def error():
    details = "Most likely, the ticker you entered was not found in the dataset."
    return render_template('error.html', culprit='Quandle', details=details)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
