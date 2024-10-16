from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']  # Get the URL from the form
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table(s) containing the list of universities
    tables = soup.find_all('table', {'class': 'wikitable'})
    universities = []

    # Iterate over the tables and extract data
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            if len(cols) > 1:
                university = {
                    "institution": cols[0].text.strip(),
                    "location": cols[1].text.strip(),
                    "type": cols[2].text.strip()
                }
                universities.append(university)

    # Save data to a JSON file
    with open('data.json', 'w') as f:
        json.dump(universities, f, indent=4)

    return render_template('index.html', universities=universities)

if __name__ == '__main__':
    app.run(debug=True)
