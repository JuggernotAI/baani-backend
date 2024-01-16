import requests

# Define the URL of your Flask app
flask_app_url = 'http://127.0.0.1:5000'  # Update with the actual URL where your Flask app is running

# Define the prompt you want to send
prompt = "Generate a creative response to this prompt."

# Create a dictionary with the prompt data
data = {'prompt': prompt}

# Send a POST request to the /generate endpoint
response = requests.post(f'{flask_app_url}/generate', json=data)

# Check the response status code and handle the response
if response.status_code == 200:
    # Extract and print the response content
    response_data = response.json()
    print(f'Response from GPT-4 API: {response_data["response"]}')
else:
    print(f'Failed to generate a response. Status code: {response.status_code}')
