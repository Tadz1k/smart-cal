from flask import Flask, render_template, request
import sys

import cal_connector

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    events_to_display = []
    events = cal_connector.get_events()
    for event in events:
        print(type(event))
        events_to_display.append(cal_connector.parse_event(event))
    
    return render_template('demo.html', events=events_to_display)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['description']
        start_time = request.form['sdate']
        end_time = request.form['edate']
        location = request.form['location']
        
        return "Name: {}, Start Time: {}, End Time: {}, Location: {} <br>Added!".format(name, start_time, end_time, location)
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
    