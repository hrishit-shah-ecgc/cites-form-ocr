from flask import Flask, render_template, request
import glob
import analyze_CHE_permits
import analyze_USA_permits
import analyze_CAN_permits
import json
import os
import time


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.jinja2')  

@app.route('/', methods=['POST'])
def login():                         
    login = request.form

    country = login['country']
    input_location = login['input_location']
    output_location = login['output_location']
    output_name = login['output_name']
    runs = login['runs']
    time_sleep = login['time']

    print(os.path.join(output_location, output_name))

    if runs == '1 Run':
        files_in_input = glob.glob(input_location + '\*.pdf')

        if country == 'CHE':
            analyze_CHE_permits.main(files_in_input, os.path.join(output_location, output_name))
        if country == 'USA':
            analyze_USA_permits.main(files_in_input, os.path.join(output_location, output_name))
        if country == 'CAN':
            analyze_CAN_permits.main(files_in_input, os.path.join(output_location, output_name))
        
    elif runs == 'Multi Run':
        while True:
            files_in_input = glob.glob(input_location + '\*.pdf')
            f = open('files.json')
            data = json.load(f)
            for file in files_in_input:
                if input_location not in data.keys():
                    data[input_location] = True
                    if country == 'CHE':
                        analyze_CHE_permits.main(files_in_input, os.path.join(output_location, output_name))
                    if country == 'USA':
                        analyze_USA_permits.main(files_in_input, os.path.join(output_location, output_name))
                    if country == 'CAN':
                        analyze_CAN_permits.main(files_in_input, os.path.join(output_location, output_name))
            time.sleep(time_sleep)


    return render_template('confirmation.jinja2', output=os.path.join(output_location, output_name))  

if __name__ == '__main__':
    app.run(debug=True)
