from flask import Flask, render_template, request, redirect, url_for
import csv
import requests
import time

app = Flask(__name__)

data_males = []
data_females = []
accepted_rows = []
current_index = 0
current_list = 1 

def read_csv(file_path):
    global data
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        return list(csv_reader)

def save_to_csv(file_path, rows):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

@app.route('/')
def index():
    global current_index, current_list, accepted_rows
    if current_list == 1:
        data = data_males
        output_file = 'accepted_husbandos.csv'
    else:
        data = data_females
        output_file = 'accepted_waifus.csv'

    if current_index < len(data):
        current_element = data[current_index][0]
        character_name = data[current_index][1]
        source = data[current_index][3]
        image_link = data[current_index][4]
        return render_template('index.html', image_link=image_link, current_element=current_element, character_name=character_name, source=source)
    else:
        save_to_csv(output_file, accepted_rows)
        accepted_rows = []
        if current_list == 1:
            current_list = 2
            current_index = 0
            return redirect(url_for('index'))
        else:
            return "All rows processed and accepted data saved for both lists."

@app.route('/action', methods=['POST'])
def action():
    global current_index, accepted_rows
    if request.form['action'] == 'accept':
        if current_list == 1:
            accepted_rows.append(data_males[current_index])
        else:
            accepted_rows.append(data_females[current_index])
    current_index += 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    data_males = read_csv('db_male.csv')
    data_females = read_csv('db_female.csv')
    app.run(debug=True)