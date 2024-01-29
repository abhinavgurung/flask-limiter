from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename
from io import BytesIO

app = Flask(__name__)
# token_credential = DefaultAzureCredential()


@app.route('/test-route')
def test_route():
    return jsonify({'message':'This is a test route'})

@app.route('/file')
def file():
    local_file_name='test.txt'
    try:
        # Sanitize the filename for security
        filename = secure_filename(local_file_name)

        # Open the file in binary mode
        with open(local_file_name, 'rb') as file:
            file_content = file.read()

        # Send the local file as a response with Content-Disposition header
        response = send_file(
            BytesIO(file_content),
            as_attachment=True,
            mimetype='text/plain',  # Adjust the mimetype as per your file type
            download_name=filename
        )

        # Set the Content-Disposition header to force download with the filename
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    except Exception as e:
        return f"Error: {str(e)}", 500
