from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def index():
    return "evolved5G echo web-server started"

@app.route('/monitoring/callback', methods=['POST'])
def location_reporter():
    print("New location retrieved:")
    print(request.get_json())
    return request.get_json()

if __name__ == '__main__':
    print("initiating")
    app.run(host='0.0.0.0')

