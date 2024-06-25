from flask import Flask, render_template, request, redirect, url_for
import csv
import requests
import time

app = Flask(__name__)

data = []
male_rows = []
female_rows = []
current_index = 0
url = 'https://graphql.anilist.co'

def read_csv(file_path):
    global data
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)

@app.route('/')
def index():
    global current_index
    if current_index < len(data):
        current_element = data[current_index][0]
        character_name = data[current_index][1] 
        source = data[current_index][3]
        image_link = data[current_index][4]
        return render_template('split.html', image_link=image_link, current_element=current_element, character_name=character_name, source=source)
    else:
        with open('db_male.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(male_rows)
        with open('db_female.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(female_rows)
        return "All rows processed and accepted data saved."

@app.route('/action', methods=['POST'])
def action():
    global current_index
    if request.form['action'] == 'male':
        male_rows.append(data[current_index])
    elif request.form['action'] == 'female':
        female_rows.append(data[current_index])
    elif request.form['action'] == 'both':
        male_rows.append(data[current_index])
        female_rows.append(data[current_index])

    current_index += 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    read_csv('db_special.csv')
    app.run(debug=True)
