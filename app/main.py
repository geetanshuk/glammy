from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/dresses")
def dresses():
    dresses_data = [
        {
            'name': 'Abstract Dream',
            'description': 'A colorful abstract painting',
            'image_url': '/static/images/black_knotted_h&m_fitted.png',
            'price': 120.00
        },
        {
            'name': 'Ocean View',
            'description': 'A serene ocean view painting',
            'image_url': '/static/images/leather_jacket_testing.png',
            'price': 95.00
        },
        # Add more paintings here...
    ]
    return render_template('dresses.html', dresses=dresses_data)


@app.route("/tops")
def tops():
    tops_data = [
        {
            'name': 'Abstract Dream',
            'description': 'A colorful abstract painting',
            'image_url': '/static/images/crochet_vest_h&m_fitted.png',
            'price': 120.00
        },
        {
            'name': 'Ocean View',
            'description': 'A serene ocean view painting',
            'image_url': '/static/images/pink_croptop_testing.webp',
            'price': 95.00
        },
        # Add more paintings here...
    ]
    return render_template('tops.html', tops=tops_data)

@app.route("/bottoms")
def bottoms():
    tops_data = [
        {
            'name': 'Abstract Dream',
            'description': 'A colorful abstract painting',
            'image_url': '/static/images/grey_cargo_testing.jpg',
            'price': 120.00
        },
        {
            'name': 'Ocean View',
            'description': 'A serene ocean view painting',
            'image_url': '/static/images/black_skort_h&m_fitted.png',
            'price': 95.00
        },
        # Add more paintings here...
    ]
    return render_template('tops.html', tops=tops_data)

if __name__ == '__main__':
    app.run(debug=True)
