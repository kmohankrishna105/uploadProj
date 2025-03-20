from flask import Blueprint, request, jsonify, send_file
import io
from models import db, breachFile  # Import db and File model

file_bp = Blueprint("file_bp", __name__)

# Upload File API
@file_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    print("Home route was accessed!")
    file = request.files['file']
    new_file = breachFile(filename=file.filename, data=file.read())

    db.session.add(new_file)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully", "file_id": new_file.id})

# Download File API
@file_bp.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    file = breachFile.query.get_or_404(file_id)

    return send_file(
        io.BytesIO(file.data),
        download_name=file.filename,  # Flask 2.x uses `download_name`
        as_attachment=True
    )
