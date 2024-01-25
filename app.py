import os
import openai
from dotenv import load_dotenv
from main import chatbot, init_chat
from instructions.system_instructions import LLM_INSTRUCTIONS
from function.linkedin_executor import make_post_linkedin
from function.twitter_executor import post_twitter
from flask import Flask, jsonify, request, session, redirect, url_for, json
from flask_cors import CORS
from requests_oauthlib import OAuth1Session
from werkzeug.utils import secure_filename
from image import verifier
load_dotenv()
client=openai

app = Flask(__name__)
CORS(app)
TEMP = '/temp'
app.secret_key = os.urandom(24)  # Generate a secret key for session management
app.config['TEMP'] = TEMP

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

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
            response = request.json
            messages = response.get("messages")
            # print(messages)
            # print(type(prompt))
            if not messages:
                return jsonify({'error': 'Missing prompt parameter'}), 400
            response = chatbot(messages)
            print(response)

            if response:
                return jsonify({'response': response}), 200
            else:
                return jsonify({'error': 'Failed to generate response'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/upload/image', methods=['POST'])
def upload_image():
    file = request.files['image']
    if not file:
        return jsonify({'error': 'Image is required'}), 400
    temp_dir = './temp'
    filename = file.filename
    file_path = os.path.join(temp_dir, filename)
    file.save(file_path)
    # file.save(tmp_file)
    # if file and verifier.allowed_file(file.filename):
    #     # os.makedirs(TEMP, exist_ok=True) # Create upload folder if it doesn't exist
    #     filename = secure_filename(file.filename)
    #     file_path = os.path.join(app.config['TEMP'], filename)
    #     file.save(file_path)
    return jsonify({'response': file_path}), 200
    # else:
    #     return jsonify({'error': 'Please provide a valid image'}), 500
    
    # url = gcs_upload_image(tmp_file) 
    # os.remove(tmp_file)
    
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
@app.route('/linkedin/post/image', methods=['POST'])
def call_linkedin():
    pass
    # file = request.files['image']
    # if not file:
    #     return jsonify({'error': 'Image is required'}), 400
    # temp_dir = './temp'
    # filename = file.filename
    # file_path = os.path.join(temp_dir, filename)
    # file.save(file_path)
    # # file.save(tmp_file)
    # # if file and verifier.allowed_file(file.filename):
    # #     # os.makedirs(TEMP, exist_ok=True) # Create upload folder if it doesn't exist
    # #     filename = secure_filename(file.filename)
    # #     file_path = os.path.join(app.config['TEMP'], filename)
    # #     file.save(file_path)
    # return jsonify({'response': file_path}), 200
    # if request.method=='POST':
    #     try:
    #         data = request.json
    #         content = data.get('content')
    #         if not content:
    #             return jsonify({'error': 'Missing content for posting on Linkedin'}), 400
    #         response = make_post_linkedin(content)

    #         if response:
    #             return jsonify({'Response': response}), 200
    #         else:
    #             return jsonify({'error': 'Internal Server Error'}), 500
    #     except Exception as e:
    #         return jsonify({'error': str(e)}), 500
@app.route('/twitter/auth/init', methods=['GET'])
def init_twitter_auth():
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    session['resource_owner_key'] = fetch_response.get('oauth_token')
    session['resource_owner_secret'] = fetch_response.get('oauth_token_secret')

    # Get authorization URL
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    return jsonify({'authorization_url': authorization_url})

@app.route('/twitter/auth/verify', methods=['POST'])
def complete_twitter_auth():
    verifier = request.json.get('verifier')
    resource_owner_key = session.get('resource_owner_key')
    resource_owner_secret = session.get('resource_owner_secret')

    # Exchange verifier for access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    # Store access tokens in session or database
    session['access_token'] = oauth_tokens['oauth_token']
    session['access_token_secret'] = oauth_tokens['oauth_token_secret']
    return jsonify({'message': 'Authentication successful'})

@app.route('/twitter/post', methods=['POST'])
def post_to_twitter():
    if request.method=='POST':
        try:
    # Retrieve access tokens
            access_token = session.get('access_token')
            access_token_secret = session.get('access_token_secret')
            if not access_token or not access_token_secret:
                return jsonify({'error': 'Authentication required'}), 401
            # Retrieve tweet text
            tweet_text = request.json.get('text')
            if not tweet_text:
                return jsonify({'error': 'Tweet text is required'}), 400
            response = post_twitter(tweet_text, access_token, access_token_secret)
            if response:
                return jsonify({'response': response}), 200
            else:
                return jsonify({'error': 'Failed to generate response'}), 500
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
