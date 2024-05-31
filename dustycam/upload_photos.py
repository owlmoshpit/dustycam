import requests
import os

#use dotenv
from dotenv import load_dotenv
load_dotenv()




from dustycam import config

# Configuration
folder_path  = config.IMAGES_FOLDER
presigning_service_url = config.dustycloud_url

# Load users token from environment variable
token = os.getenv('DUSTYCLOUD_TOKEN')
print(token)


def get_presigned_url(file_name):
    #add header with authorization token
    headers = {
        'Authorization': 'Bearer <YOUR_TOKEN>'
    }

    response = requests.post(presigning_service_url, json={'file_name': file_name}, headers=headers)

    if response.status_code == 200:
        return response.json()['url']
    else:
        print(f"Failed to get presigned URL. Status code: {response.status_code}")
        print("Response:", response.text)
        return None

def upload_file(file_path, upload_url):
    with open(file_path, 'rb') as file:
        print(f"Uploading file {file_path}...")

        #add header content type
        headers = {
            'Content-Type': 'image/jpeg'
        }


        response = requests.put(upload_url, files={'file': file}, headers=headers)

        print(response.__dict__)

        if response.status_code == 200:
            print("File uploaded successfully.")
            os.remove(file_path)
            print("File deleted.")
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
            print("Response:", response.text)

if __name__ == '__main__':

    #get the first file in the folder
    files = os.listdir(folder_path)
    if len(files) == 0:
        print(f"No files found in {folder_path}")
        exit()
    
    file_path = os.path.join(folder_path, files[0])
    
    file_name = f'test/{files[0]}'
    upload_url = get_presigned_url(file_name)


    if os.path.exists(file_path):
        upload_file(file_path, upload_url)
    else:
        print(f"File {file_path} does not exist.")