import os
import sys
sys.path.append('api')

try:
    from flask import Flask
    from flask_cors import CORS
    from controllers import health_controller, chat_controller
    from config import Config
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'https://*'])
    
    try:
        from services.database_service import init_database
        init_database()
        print("✅ Database initialization completed")
    except Exception as e:
        print(f"⚠️  Database initialization failed: {e}")
    
    app.register_blueprint(health_controller.bp)
    app.register_blueprint(chat_controller.chat_controller)
    
    return app

if __name__ == '__main__':
    print("🚀 Starting Flask development server...")
    app = create_app()
    app.run(host='0.0.0.0', port=Config.PORT, debug=False)

# Create app instance for Gunicorn
print("🚀 Creating app for Gunicorn...")
app = create_app()
print("✅ App created successfully")
