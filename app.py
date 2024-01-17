from flask import Flask, request, jsonify
from main import chatbot

app = Flask(__name__)

# Replace with your GPT-4 API function
# def get_response_openai(prompt):
#     # Implement your function to call GPT-4 API and return the response
#     # Example implementation:
#     # response = some_function_to_call_gpt4_api(prompt)
#     response = "This is a placeholder response"
#     return response

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        # Get the prompt from the POST request
        data = request.json
        prompt = str(data.get('prompt'))
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

if __name__ == '__main__':
    app.run(debug=True)
