import requests
import json

url = 'http://127.0.0.1:5000/upload/image'

my_img = {'image': open('test.jpg', 'rb')}

response = requests.post(url, files=my_img)

# Check the response status code and handle the response
if response.status_code == 200:
    # Extract and print the response content
    response = response.json()
    data = response.get('response')
    # response_data = response.get("response")

    print(data)
else:
    print(f'Failed to generate a response. Status code: {response.status_code}')