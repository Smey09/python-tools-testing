
from flask import Flask, render_template, request, redirect, url_for
import json
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Load data from data.json
def load_data():
    """Load data from JSON file."""
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    return {"data": []}  # Return an empty list by default

@app.route('/')
def input_page():
    """Render the input form page."""
    return render_template('input.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    """Scrape data from the provided URL."""
    print("Scrape route accessed")  # Debugging line
    url = request.form['url']
    
    # Calculate the length of the border line based on the URL length
    border_length = len(f"Submitted URL: {url}") + 4  # 4 for the " | " padding
    # Print the top border
    print("+" + "-" * (border_length - 2) + "+")
    # Print the URL message
    print(f"\033[34m| Submitted URL: {url} |\033[0m")
    # Print the bottom border
    print("+" + "-" * (border_length - 2) + "+")


    scraped_data = []  # This will store all scraped data

    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Identify all tables on the page
        tables = soup.find_all('table')

        for table in tables:
            rows = table.find_all('tr')
            if not rows:
                continue
            
            # Assume the first row contains headers
            header_cells = rows[0].find_all('th')
            headers = [th.text.strip() for th in header_cells]

            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                if len(cols) == len(headers):  # Ensure the number of columns matches
                    entry = {}
                    for index, col in enumerate(cols):
                        entry[headers[index]] = col.text.strip()
                    
                    scraped_data.append(entry)

        # Save data to a JSON file
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({"data": scraped_data}, f, ensure_ascii=False, indent=4)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "An error occurred while scraping the URL.", 400

    # Redirect to index page with the scraped data
    return redirect(url_for('index'))

@app.route('/data')
def index():
    """Render the page to display scraped data."""
    data = load_data()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
