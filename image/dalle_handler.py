import os
import requests
from urllib.parse import urlparse
from datetime import datetime
temp_dir = "temp"
def dalle_handler(url=None):
    if url:
        pass
        # try:
        #     print("this is your url", url)
        #     response = requests.get(url)
        #     if response.status_code == 200:
        #         # Parse the URL to get the image name or use a timestamp
        #         image_name = os.path.basename(urlparse(url).path)
        #         if not image_name:
        #             # If the URL does not contain an image name, use a timestamp
        #             image_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
                
        #         # Complete file path
        #         file_path = os.path.join(temp_dir, image_name)

        #         # Write the image to a file
        #         with open(file_path, 'wb') as file:
        #             file.write(response.content)
        #         print(f"Image saved to {file_path}")
        #     else:
        #         print("Failed to download the image: Status code", response.status_code)
        # except requests.RequestException as e:
        #     print("Error while downloading the image:", e)
