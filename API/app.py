from datetime import datetime

from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for Vue.js frontend

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# File Model
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for file creation
    fut_contract = db.Column(db.String(255))  # A contract identifier or reference
    last_update_time = db.Column(db.DateTime)  # Timestamp for position updates
    size = db.Column(db.Integer)  # File size in bytes
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of upload
    filename = db.Column(db.String(255))
    data = db.Column(db.LargeBinary)  # Store the file content

# Create database tables
with app.app_context():
    db.create_all()

# Upload File API
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    new_file = File(filename=file.filename, data=file.read())

    db.session.add(new_file)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully", "file_id": new_file.id})

# Download File API
@app.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    file = File.query.get_or_404(file_id)

    return send_file(
        io.BytesIO(file.data),  # Convert the binary data to a byte stream
        attachment_filename=file.filename,
        as_attachment=True
    )
if __name__ == '__main__':
    app.run(debug=True)
