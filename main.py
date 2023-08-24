import hashlib
from contextlib import contextmanager
import requests
import os
import time
from flask import Flask, request, render_template, render_template_string, send_file
from apscheduler.schedulers.background import BackgroundScheduler
from markupsafe import escape
from dotenv import load_dotenv
from cachetools import LRUCache

# Create an LRU cache with a maximum size
cache = LRUCache(maxsize=100)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static')

'''
csp_policy = {
    'default-src': ['self'],
    'script-src': ['self'],
    'style-src': ['self', "'unsafe-inline'"],
    'style-src-elem': ['self', "'unsafe-inline'"],
    'img-src': ['self']
    # Add more directives as needed
}


@app.after_request
def add_security_headers(response):
    csp_value = "; ".join([f"{directive} {' '.join(sources)}" for directive, sources in csp_policy.items()])
    response.headers['Content-Security-Policy'] = csp_value
    return response
'''


def cleanup_images(directory, max_age_hours):
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > max_age_seconds:  # Compare with max_age_seconds, not multiplied value
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")


@contextmanager
def create_qrcode(content):
    content_hash = hashlib.sha1(content.encode()).hexdigest()
    filename = f"qrcode_{content_hash}.png"
    try:
        # Existing code for API request and saving the image
        yield filename
    finally:
        cache[content_hash] = filename


def make_qrcode(content):
    with create_qrcode(content) as filename:
        try:
            rapidapi_key = os.environ.get("RAPIDAPI_KEY")
            if not rapidapi_key:
                raise ValueError("RapidAPI key not found in environment variables")

            url = "https://easy-qr-code.p.rapidapi.com/generate"
            querystring = {"content": content}

            headers = {
                "X-RapidAPI-Key": rapidapi_key,
                "X-RapidAPI-Host": "easy-qr-code.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()

            if "image/png" not in response.headers.get("content-type", ""):
                raise ValueError("API response is not a valid PNG image")

            image_data = response.content
            with open(os.path.join('static', filename), "wb") as f:
                f.write(image_data)
            print(f"QR code saved as {filename}")
            return filename
        except requests.exceptions.RequestException as e:
            raise Exception("Error while making API request: " + str(e))


@app.route('/', methods=['GET', 'POST'])
def index():
    image_filename = None
    error_message = None

    if request.method == 'POST':
        input_data = escape(request.form.get('input_data'))  # Sanitize the input
        if not input_data:
            error_message = "Please enter a URL."
        else:
            try:
                image_filename = make_qrcode(input_data)
            except Exception as e:
                error_message = "An error occurred while generating the QR code. Please try again."
                print("Error:", str(e))

    return render_template('index.html', image_filename=image_filename, error_message=error_message)


@app.route('/show_qrcode/<filename>')
def show_qrcode(filename):
    full_path = os.path.join(app.root_path, 'static', filename)  # Construct full path to the image
    return send_file(full_path, mimetype='image/png')


if __name__ == '__main__':
    image_directory = 'static'
    max_age_hours = 0.2
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_images, 'interval', hours=24, args=[image_directory, max_age_hours])
    scheduler.start()

    app.run(debug=True)
