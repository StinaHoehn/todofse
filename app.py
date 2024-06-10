from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
from flask_cors import CORS

# create a new Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS

# create a MongoClient instance to connect to the MongoDB server
client = MongoClient("mongodb://mongo:27017")

# database instance
db = client["mydatabase"]

# collection instance
todos = db["Todos"]

# Your OpenWeatherMap API key
WEATHER_API_KEY = '2321d60237674c67b4595038241006'

# API endpoint to get todos data
@app.route('/todos', methods=['GET'])
def get_todos():
    todos_data = []
    for todo_element in todos.find():
        todos_data.append({
            "id": str(todo_element["_id"]),
            "name": todo_element["name"],
            "description": todo_element["description"],
            "status": todo_element["status"],
            "tags": todo_element["tags"]
        })
    return jsonify(todos_data), 200

# API endpoint to add customer data
@app.route('/todos', methods=['POST'])
def add_todos():
    new_todo = {
        "name": request.json["name"],
        "description": request.json["description"],
        "status": request.json["status"],
        "tags": request.json["tags"]
    }
    x = todos.insert_one(new_todo)
    return jsonify({"id": str(x.inserted_id)}), 201

# API endpoint to get weather data
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', default='London')
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json()), response.status_code
    else:
        return jsonify({"error": "Unable to fetch weather data"}), response.status_code

# API default endpoint
@app.route('/', methods=['GET'])
def default():
    return "Welcome to the Todo API!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
