from flask import Flask, render_template
import json
import os # Added to construct path safely

app = Flask(__name__)

# Determine the base directory of the 'app' folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEWS_DATA_PATH = os.path.join(BASE_DIR, 'news_data.json')

@app.route('/')
def home():
    articles_data = []
    error_msg = None
    try:
        # Corrected path to be relative to the app directory
        with open(NEWS_DATA_PATH, 'r') as f:
            articles_data = json.load(f)
    except FileNotFoundError:
        error_msg = f"Error: The news data file ({os.path.basename(NEWS_DATA_PATH)}) was not found. Please run the scraper script first."
        print(f"Error: {NEWS_DATA_PATH} not found.")
    except json.JSONDecodeError:
        error_msg = "Error: Could not decode the news data. The JSON file might be corrupted."
        print(f"Error: JSONDecodeError while reading {NEWS_DATA_PATH}.")
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        print(f"An unexpected error occurred: {e}")
        
    return render_template('index.html', articles=articles_data, error_message=error_msg)

if __name__ == '__main__':
    # Making sure the app runs on 0.0.0.0 to be accessible
    # and using a common port like 5000.
    # Debug is True for development.
    app.run(host='0.0.0.0', port=5000, debug=True)
