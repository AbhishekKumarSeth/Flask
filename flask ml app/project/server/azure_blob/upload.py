
from flask import Blueprint, request, redirect, make_response, jsonify

from project.server.auth.views import auth_required
from project.server.app import app, db
from project.server.dbmodel.documentmodel import Dcoument, Category, DocumentSchema

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.storage.blob import generate_blob_sas, AccountSasPermissions
from werkzeug.utils import secure_filename
import datetime
from datetime import datetime, timedelta
import string, random, requests
import os
import json
from marshmallow import ValidationError


azure_blueprint = Blueprint('azure', __name__)


app.config.from_pyfile('config.py')
account = app.config['STORAGE_ACCOUNT_NAME']   # Azure account name
key = app.config['ACCOUNT_KEY']      # Azure Storage account access key  
connect_str = app.config['CONNECTION_STRING']
container_name = app.config['CONTAINER_NAME'] # Container name

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container = ContainerClient.from_connection_string(connect_str, container_name)


def index():
    return "Flask API is running"


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

def update_documentdetails_to_db(display_file_name, file_name, catagory):
    docdetails = Dcoument(
                display_file_name = display_file_name,
                file_name=file_name,
                category = catagory
            )
    db.session.add(docdetails)
    db.session.commit()

    return docdetails.id


@auth_required
def upload_file(category):
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            display_file_name = filename
            now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
            filename = now + '__' + filename
            
            file.save(filename)

            create_container_if_not_exist()

            blob_client = blob_service_client.get_blob_client(container = container_name, blob = filename)
            msg = ''
            with open(filename, "rb") as data:
                try:
                    blob_client.upload_blob(data, overwrite=True)
                    documentId = update_documentdetails_to_db(display_file_name, filename, category)
                    if documentId is not None:
                        msg = "Upload Done ! "
                    else:
                        msg = "upload fail"
                except Exception as e:
                    print(e)
            os.remove(filename)

            return msg


# @auth_required
def download_blob(doc_id):
    try:
        blob_client = blob_service_client.get_blob_client(container = container_name, blob = "0266554465.jpeg")

        # return blob_client.download_blob().readall()
        doc_detail = Dcoument.query.get(doc_id)
        if doc_detail:
            blob_name = doc_detail.file_name
            print(blob_name)
            url = f"https://{account}.blob.core.windows.net/{container_name}/{blob_name}"
            sas_token = generate_blob_sas(
                account_name=account,
                account_key=key,
                container_name=container_name,
                blob_name=blob_name,
                permission=AccountSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1)
            )
        url_with_sas = f"{url}?{sas_token}"
        return redirect(url_with_sas)
    except Exception as ex:
        print(ex)


# @auth_required
def get_all_blob_list_from_db():
    try:
        docs = Dcoument.query.all()
        print(docs)
        docs_schema = DocumentSchema(many=True)

        # print(docs_schema.validate(docs)) ##{0: {'_schema': ['Invalid input type.']}}
        
        results = docs_schema.dump(docs)

        # results = [
        #     {
        #         "id":doc.id,
        #         "display_file_name": doc.display_file_name,
        #         "file_name": doc.file_name,
        #         "category": doc.category
        #     } for doc in docs]

        return {"count": len(results), "data": results}
    except Exception as ex:
        print(ex)
        return ex


# add Rules for API Endpoints
azure_blueprint.add_url_rule('/', view_func=index, methods=['GET'])
azure_blueprint.add_url_rule('/uploader/<category>', view_func=upload_file, methods=['POST'])
azure_blueprint.add_url_rule('/download/<doc_id>', view_func=download_blob, methods=['GET'])
azure_blueprint.add_url_rule('/documentlist', view_func=get_all_blob_list_from_db, methods=['GET'])