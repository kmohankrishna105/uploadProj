import os
from datetime import datetime

from flask import Blueprint, request, jsonify, send_file
import io
from models import db, BreachDocument  # Import db and File model

file_bp = Blueprint("file_bp", __name__)


@file_bp.route('/', methods=['GET'])
def get_files():
    print("get function started")
    files = BreachDocument.query.all()  # Fetch all files
    print(files)
    if not files:
        return jsonify({"error": "No records found"}), 404  # If empty, return 404
    for file in files:
        print(file.to_json())

    print("Get Function ended")
    return jsonify([file.to_json() for file in files])

# Upload File API
@file_bp.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    print("SUUUUUUUUUUUUUUUUUUUUUUUUUUPER")
    file_id = request.form.get("file_id") or (request.json.get("file_id") if request.is_json else None)
    print("BABUUUUUUU",file_id)
    #print("VARS",vars(request))
    print(file_id)
    print("SUUUUUUUUUUUUUUUUUUUUUUUUUUPER2")
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    print("Home route was accessed!")
    file = request.files['file']
    #is_verified = request.form.get("is_verified", "false").lower() == "true"

    file_data = file.read()  # ✅ Read file data once
    existing_file = BreachDocument.query.get(file_id)  # ✅ Fetch the existing file
    print(existing_file.id)
    print(file.filename)
    # ✅ Update existing file record
    existing_file.filename = file.filename
    existing_file.data = file_data
    #existing_file.size = len(file_data)
    #existing_file.uploaded_at = datetime.utcnow()
    print("!@#$%^&*()@#$%^&*",type(existing_file))
    print("!@#$%^&*()@#$%^&*",existing_file.filename)
    #print("!@#$%^&*()@#$%^&*",existing_file.uploaded_at)

    #new_file = breachFile(filename=file.filename, data=file.read(),
    #size = len(file.read()),
    #uploaded_at = datetime.utcnow(),
    #is_verified = is_verified,)

    #db.session.add(new_file)
    db.session.commit()

    return jsonify({"message": "File uploaded successfully"})


@file_bp.route('/records', methods=['GET'])
def true_records():
    print("Genuine function started")
    files = BreachDocument.query.filter(BreachDocument.is_genuine == True).all()
    if not files:
        return jsonify({"error": "No records found"}), 404

    print("records function ended")
    return jsonify([file.to_json() for file in files])


@file_bp.route('/Update', methods=['PUT'])
def update_records():
    print("update_records method")
    print("VARS------updates",vars(request))
    data=request.get_json()
    file_id=data.get("file_id")
    is_genuine = data.get("is_genuine")
    remarks = data.get("remarks")

    print("VAAAAARS",vars(request))
    print("file_id",file_id)
    print("is_genuinessssssss",is_genuine)

    if not file_id or is_genuine is None or remarks is None:
        return jsonify({"error": "Missing required fields"}), 400

    existing_file = BreachDocument.query.get(file_id)  # ✅ Fetch the existing file

    print(is_genuine)
    if not existing_file:
        return jsonify({"error": "File not found"}), 404

    existing_file.is_genuine= is_genuine
    existing_file.remarks = remarks
    print(existing_file.is_genuine)
    db.session.commit()
    return jsonify({"message": "Is Genuine value successfully"})


@file_bp.route('/downwwload/<int:file_id>', methods=['GET'])
def download_file_old(file_id):
    file = BreachDocument.query.get_or_404(file_id)

    return send_file(
        io.BytesIO(file.data),
        download_name=file.filename,  # Flask 2.x uses `download_name`
        as_attachment=True
    )

@file_bp.route('/download', methods=['GET'])
def download_file():
    print("Download records method")
    print("VARS------downloade", vars(request))
    #data = request.get_json()
    #file_id = data.get("file_id")
    file_id = request.args.get('file_id')
    print(file_id)

    file = BreachDocument.query.get_or_404(file_id)

    return send_file(
        io.BytesIO(file.data),
        download_name=file.filename,
        as_attachment=True
    )