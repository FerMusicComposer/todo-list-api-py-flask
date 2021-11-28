"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from todos import todos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/get-todos', methods=['GET'])
def get_todos():
    response_body = {
        "msg": "Full list of To-Do's",
        "todos": todos
    }

    return jsonify(response_body), 200

# Use Postman or similar to add to-do
@app.route('/post-todo', methods=['POST'])
def post_todo():
    done = request.json['done']
    label = request.json['label']
    new_todo = {
        "done": done,
        "label": label,
    }
    todos.append(new_todo)
    response_body = {
        "msg": "ToDo added successfully",
        "todos": todos
    }

    return jsonify(response_body), 200

# Use Postman or similar to remove to-do
@app.route('/delete-todo/<int:position>', methods=['DELETE'])
def delete_todo(position):
    todo_found = todos[position]
  
    todos.remove(todo_found)
    
    response_body = {
        "msg": "ToDo deleted successfully",
        "todo_deleted": todo_found,
        "todos": todos
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
