from flask import Flask
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
#CORS(app)
#CORS(app, resources={r"/api/*": {"origins": "http://localhost:8084"}}, supports_credentials=True) # Enable CORS for Vue.js frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import models and initialize database
from models import db
db.init_app(app)


# Import and register Blueprint
from file_routes import file_bp
app.register_blueprint(file_bp, url_prefix="/api/files")

# Run Flask App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created before running
    app.run(debug=True)