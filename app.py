import os
import openai
from dotenv import load_dotenv
import json
from flask import Flask, request, jsonify
from main import chatbot
from function.linkedin_executor import make_post_linkedin
from flask import Flask, jsonify, request, session, redirect
from flask_cors import CORS
load_dotenv()
client=openai

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return {"Message": "Hello World"}
# if __name__ == "__main__":
#   pretty_print_conversation(messages=None, message="Start chatting with Baani. You can ask Baani to create content and image for Linkedin. \nBaani has the ability to post on your behalf as well( after you approval)  (type 'quit' to stop)!")
#   chatbot()
@app.route('/generate', methods=['POST'])
def generate_response():
    if request.method=='POST':
        try:
            # Get the prompt from the POST request
            data = request.json
            print(data)

            # app.logger.info(f"{data}")
            # print(data)
            prompt = data.get('prompt')
            print(type(prompt))
            if not prompt:
                return jsonify({'error': 'Missing prompt parameter'}), 400

            # Call your GPT-4 API function to get the response
            response = chatbot(prompt)

            if response:
                return jsonify({'response': response}), 200
            else:
                return jsonify({'error': 'Failed to generate response'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500
@app.route('/post_linkedin', methods=['POST'])
def call_linkedin():
    if request.method=='POST':
        try:
            data = request.json
            content = data.get('content')
            if not content:
                return jsonify({'error': 'Missing content for posting on Linkedin'}), 400
            response = make_post_linkedin(content)

            if response:
                return jsonify({'Response': response}), 200
            else:
                return jsonify({'error': 'Internal Server Error'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # prompt = "Create a tweet for Porsche 911"
    app.run(debug=True)
    # response = chatbot(prompt)
    # print(response)
