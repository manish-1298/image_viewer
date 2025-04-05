from flask import Flask, render_template, request
import requests
from io import BytesIO
from PIL import Image
import base64

app = Flask(__name__, template_folder='.')

def fetch_image(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    images = []
    if request.method == 'POST':
        urls = request.form.get("urls")
        if urls:
            urls = urls.split("\n")
            for url in urls:
                url = url.strip()
                img_data = fetch_image(url)
                if img_data:
                    images.append((img_data, url))  # Ensure it passes as a tuple
    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)
