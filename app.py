from flask import Flask, jsonify
from flask_db import get_db

app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]


#http://127.0.0.1:5000/stops/1952/78
@app.get("/stops/<int:stop_id>/<int:line_id>")
def get_stop_arrives(stop_id, line_id):
    db = get_db()
    arrive = db.get_arrive((stop_id, line_id))
    return jsonify(arrive)
