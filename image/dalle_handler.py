import os
import requests

def dalle_handler(url=None):
    file_path="./temp"
    if url:
        response = requests.get(url)
        if response.status_code == 200:
        # Write the image to a file
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Image saved to {file_path}")
        else:
            print("Failed to download the image")