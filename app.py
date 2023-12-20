from flask import Flask, jsonify
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)
# token_credential = DefaultAzureCredential()

# Your Azurite local connection string
connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

@app.route('/create_container')
def create_container():
    container_name = "cdcontainer1"

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


        return f"Container '{container_name}' created successfully."

    except Exception as e:
        print('caught exception')
        print(str(e))
        return f"Error: {str(e)}"


@app.route('/test-route')
def test_route():
    return jsonify({'message':'This is a test route'})