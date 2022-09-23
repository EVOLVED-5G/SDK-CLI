from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def index():
    return "evolved5G echo web-server started"

@app.route('/monitoring/callback', methods=['POST'])
def handle_callback_notification():
    print("New notification retrieved:")
    print(request.get_json())
    return request.get_json()

#  for loss of connectivity if we want to


if __name__ == '__main__':
    print("initiating")
    app.run(host='0.0.0.0')

