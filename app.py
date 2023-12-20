from flask import Flask, jsonify, request
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)
# token_credential = DefaultAzureCredential()

# Your Azurite local connection string
connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

@app.route('/create_container')
def create_container():
    container_name = "cdcontainer2"

    try:
        # Create a BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Create a new container
        container_client = blob_service_client.get_container_client(container_name)
        container_client.create_container()
        print(f"Container '{container_name}' created successfully.")

        # Fetch the list of containers
        containers = blob_service_client.list_containers()

        # Extract container names and create a list
        container_names = [container.name for container in containers]
        print('---- container names-----')
        print(container_names)

        # Get the file from the request
        uploaded_file = request.files['file']

        if uploaded_file:
            container_name = "your-container-name"
            file_name = uploaded_file.filename



        return f"Container '{container_name}' created successfully."

    except Exception as e:
        print('caught exception')
        print(str(e))
        return f"Error: {str(e)}"


@app.route('/upload_blob', methods=['POST'])
def upload_blob():
    try:
        # Get the file from the request
        uploaded_file = request.files['file']

        if uploaded_file:
            container_name = "cdcontainer"
            file_name = uploaded_file.filename

            # Create a BlobServiceClient using the connection string
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)

            # Get or create the container
            container_client = blob_service_client.get_container_client(container_name)
            # container_client.create_container()

            # Get the BlobClient for the uploaded file
            blob_client = container_client.get_blob_client(file_name)

            # Upload the file/blob
            blob_client.upload_blob(uploaded_file)

            return jsonify({"message": f"File '{file_name}' uploaded successfully to '{container_name}'"})

    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/test-route')
def test_route():
    return jsonify({'message':'This is a test route'})