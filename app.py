import os
import openai
from dotenv import load_dotenv
from main import chatbot, init_chat
from instructions.system_instructions import LLM_INSTRUCTIONS
from function.linkedin_executor import make_post_linkedin
# from function.twitter_executor import get_verifier, attach_verifier
from flask import Flask, jsonify, request, session, redirect, url_for, json
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
@app.route('/chat/init', methods=['GET'])
def init_chat_call():
    messages_str = init_chat()
    messages_json = {"messages": messages_str}

    print(type(messages_json))
    return messages_json
@app.route('/chat/generate', methods=['POST'])
def generate_response():
    if request.method=='POST':
        try:
            # Get the prompt from the POST request
            
            response = request.json
            messages = response.get("messages")
            print(messages)

            
            # print(type(prompt))
            if not messages:
                return jsonify({'error': 'Missing prompt parameter'}), 400

            # Call your GPT-4 API function to get the response
            response = chatbot(messages)

            if response:
                return jsonify({'response': response}), 200
            else:
                return jsonify({'error': 'Failed to generate response'}), 500
            return "Success!"
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

# @app.route('/twitter/authenticate')
# def twitter_authenticate():
#     authorization_url, resource_owner_key, resource_owner_secret = get_verifier()
#     session[resource_owner_key] = resource_owner_key
#     session[resource_owner_secret] = resource_owner_secret
#     session[authorization_url] = authorization_url
#     return redirect(authorization_url)
# @app.route('/twitter/callback')
# def twitter_callback():
#     verifier = request.args.get('oauth_verifier')
#     resource_owner_key = session[resource_owner_key]
#     resource_owner_secret = session[resource_owner_secret]
#     authorization_url = session[authorization_url]
#     access_token, access_token_secret = attach_verifier(
#         authorization_url, resource_owner_key, resource_owner_secret, verifier
#     )
#     access_token = session[access_token]
#     access_token_secret = session[access_token_secret]
#     # You can save the access tokens here or use them to make API calls.
#     return "Authorization successful!"
# @app.route('/twitter/post')
# def twitter_post():



if __name__ == '__main__':
    # prompt = "Create a tweet for Porsche 911"
    app.run(debug=True)
    # response = chatbot(prompt)
    # print(response)
