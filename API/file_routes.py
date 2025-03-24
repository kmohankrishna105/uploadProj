from datetime import datetime

from flask import Blueprint, request, jsonify, send_file
import io
from models import db, BreachDocument  # Import db and File model

file_bp = Blueprint("file_bp", __name__)


@file_bp.route('/', methods=['GET'])
def get_files():
    print("get function started")
    files = BreachDocument.query.all()  # Fetch all files

    if not files:
        return jsonify({"error": "No records found"}), 404  # If empty, return 404

    #print("Fetched files:", [file.to_json() for file in files])  # ✅ Debugging log
    print("Get dunction ended")
    return jsonify([file.to_json() for file in files])

# Upload File API
@file_bp.route('/upload', methods=['POST','OPTIONS'])
def upload_file():
    print("SUUUUUUUUUUUUUUUUUUUUUUUUUUPER")
    #print("1234567890",request.json)
    file_id = request.form.get("id") or (request.json.get("id") if request.is_json else None)
    #file_id=15
    print(file_id)
    print("SUUUUUUUUUUUUUUUUUUUUUUUUUUPER2")
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    print("Home route was accessed!")
    #print(request.form)
    #print("file",file)
    file = request.files['file']

    #is_verified = request.form.get("is_verified", "false").lower() == "true"

    #file = request.files["file"]
    file_data = file.read()  # ✅ Read file data once
    existing_file = BreachDocument.query.get(file_id)  # ✅ Fetch the existing file
    print(existing_file.id)
    print(file.filename)
    # ✅ Update existing file record
    existing_file.filename = file.filename
    existing_file.data = file_data
    existing_file.size = len(file_data)
    existing_file.uploaded_at = datetime.utcnow()
    print("!@#$%^&*()@#$%^&*",type(existing_file))
    print("!@#$%^&*()@#$%^&*",existing_file.filename)
    print("!@#$%^&*()@#$%^&*",existing_file.uploaded_at)

    #new_file = breachFile(filename=file.filename, data=file.read(),
    #size = len(file.read()),
    #uploaded_at = datetime.utcnow(),
    #is_verified = is_verified,)

    #db.session.add(new_file)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully"})


@file_bp.route('/<int:file_id>', methods=['GET'])
def get_file(file_id):
    file = BreachDocument.query.get(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404
    return jsonify(file.to_json())

@file_bp.route('/model', methods=['POST'])
def update_document():
    data = request.json
    file_id = data.get("id")

    if not file_id:
        return jsonify({"error": "File ID is missing"}), 400

    document = BreachDocument.query.get(file_id)

    if not document:
        return jsonify({"error": "Record not found"}), 404

    document.is_genuine = bool(data.get("is_genuine", False))  # ✅ Convert to boolean
    db.session.commit()

    return jsonify({"message": "Record updated successfully"})

# Download File API
@file_bp.route('/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    file = BreachDocument.query.get_or_404(file_id)

    return send_file(
        io.BytesIO(file.data),
        download_name=file.filename,  # Flask 2.x uses `download_name`
        as_attachment=True
    )


@file_bp.route('/records', methods=['GET'])
def true_records():
    print("true_records function started")
    files = BreachDocument.query.filter(BreachDocument.is_genuine == True).all()


    if not files:
        return jsonify({"error": "No records found"}), 404  # If empty, return 404

    #print("Fetched files:", [file.to_json() for file in files])  # ✅ Debugging log
    print("records function ended")
    return jsonify([file.to_json() for file in files])
