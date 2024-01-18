from flask import Flask, request, jsonify
from main import chatbot
from flask import Flask, jsonify, request, session, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"Message": "Hello WOrld"}

if __name__=="__main__":
    app.run(debug=True)