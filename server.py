# Smart Door Lock - Face Recognition Server
# Main entry point

from flask import Flask
from flask_cors import CORS
from config import HOST, PORT, DEBUG
from routes import api
import database

def create_app():
    """Create and configure the Flask application"""
    application = Flask(__name__)
    CORS(application)
    
    # Register routes
    application.register_blueprint(api)
    
    # Load database on startup
    database.load_faces()
    database.load_logs()
    
    return application

# Create app instance for Gunicorn (cloud deployment)
app = create_app()


def main():
    """Main entry point"""
    print("\n" + "=" * 50)
    print("   Smart Door Lock - Face Recognition Server")
    print("=" * 50)
    
    # Load existing data
    database.load_faces()
    database.load_logs()
    
    # Create app
    app = create_app()
    
    # Print startup info
    print(f"\n[*] Server starting on http://{HOST}:{PORT}")
    print(f"[*] Registration UI: http://localhost:{PORT}/register-ui")
    print(f"[*] Full App UI:     http://localhost:{PORT}/app")
    print("\n[*] Endpoints:")
    print("   POST /register  - Register new face")
    print("   POST /verify    - Verify face (ESP32)")
    print("   GET  /faces     - List registered faces")
    print("   GET  /logs      - View access history")
    print("=" * 50 + "\n")
    
    # Run server
    app.run(host=HOST, port=PORT, debug=DEBUG)


if __name__ == '__main__':
    main()
