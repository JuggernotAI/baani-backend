import requests
import os
from urllib.parse import urlparse
from datetime import datetime
temp_dir = "temp"

def make_post_linkedin(text, pic=None):
    body = {
        "access_token": os.getenv("LINKEDIN_ACCESS_TOKEN"),
        "linkedin_id": os.getenv("LINKEDIN_ID"),
        "content": text,
    }
 
    url = "https://replyrocket-flask.onrender.com/upload"
 
    try:
        if pic is None:
            response = requests.post(url, data=body, timeout=10000)
            if response.status_code == 200:
                return "Post successful!"
            else:
                return f"Failed to post. Status code: {response.status_code}"
        else:
            try:
                response = requests.get(pic)
                if response.status_code == 200:
                    
                    image_name = os.path.basename(urlparse(pic).path)
                    if not image_name:
                        image_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
                    
                    file_path = os.path.join(temp_dir, image_name)

                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Image saved to {file_path}")

                    with open(file_path, "rb") as file:
                        files = {"file": file}
                        response = requests.post(url, files=files, data=body, timeout=10000)
                        if response.status_code == 200:
                            return "We have successfully posted the post on Linkedin!"
                        else:
                            return f"Failed to post. Status code: {response.status_code}"
                else:
                    print("Failed to download the image: Status code", response.status_code)
            except requests.RequestException as e:
                print("Error while downloading the image:", e)
    except Exception as e:
        return f"An error occurred: {str(e)}"
 
