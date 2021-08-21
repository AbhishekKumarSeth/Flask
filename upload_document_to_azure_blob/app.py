import os
from flask import Flask, request, redirect, url_for
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, AccountSasPermissions
from werkzeug.utils import secure_filename
import string, random, requests
from flask_cors import CORS
import datetime
from datetime import timedelta

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

app.config.from_pyfile('config.py')
account = app.config['STORAGE_ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = app.config['CONNECTION_STRING']
container_name = app.config['CONTAINER_NAME'] # Container name

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container = ContainerClient.from_connection_string(connect_str, container_name)

def create_container_if_not_exist():
    try:
        container_properties = container.get_container_properties()
        # Container exists. You can now use it.
    except Exception as e:
        # Container does not exist. You can now create it.
        container_client = blob_service_client.create_container(container_name)


### NOT TESTED
def delete_contaiener_if_exist():
    try:
        container_properties = container.get_container_properties()
        # Container exists. You can now use it.
        container.delete_container()
    except Exception as e:
        # Container does not exist. You can now create it.
        container_client = blob_service_client.create_container(container_name)


@app.route('/')
def index():
    return 'Flask API is running'


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(filename)

            create_container_if_not_exist()

            blob_client = blob_service_client.get_blob_client(container = container_name, blob = filename)
            with open(filename, "rb") as data:
                try:
                    blob_client.upload_blob(data, overwrite=True)
                    msg = "Upload Done ! "
                except Exception as e:
                    print(e)
            os.remove(filename)

            return msg

### NOT TESTED
@app.route('/list')
def list_blob():
    data = []
    try:
        blob_list = container.list_blobs()
        for blob in blob_list:
            data.append({'filename':blob.name})
            print("\t" + blob.name)

        return data[0]

    except Exception as ex:
        print(ex)


@app.route('/download')
def download_blob():
    try:
        blob_client = blob_service_client.get_blob_client(container = container_name, blob = "0266554465.jpeg")

        # return blob_client.download_blob().readall()
        blob_name = "0266554465.jpeg"
        url = f"https://{account}.blob.core.windows.net/{container_name}/{blob_name}"
        sas_token = generate_blob_sas(
            account_name=account,
            account_key=key,
            container_name=container_name,
            blob_name=blob_name,
            permission=AccountSasPermissions(read=True),
            expiry=datetime.datetime.utcnow() + timedelta(hours=1)
        )

        url_with_sas = f"{url}?{sas_token}"
        return redirect(url_with_sas)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    app.run(debug=True)