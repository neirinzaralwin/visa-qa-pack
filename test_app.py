import os
import sys

print("🔍 Testing basic imports...")

try:
    import flask
    print("✅ Flask imported successfully")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")

try:
    import flask_cors
    print("✅ Flask-CORS imported successfully")
except ImportError as e:
    print(f"❌ Flask-CORS import failed: {e}")

print("🔍 Testing API imports...")
sys.path.append('api')

try:
    from controllers import health_controller
    print("✅ Health controller imported successfully")
except ImportError as e:
    print(f"❌ Health controller import failed: {e}")

try:
    from controllers import chat_controller
    print("✅ Chat controller imported successfully")
except ImportError as e:
    print(f"❌ Chat controller import failed: {e}")

print("🔍 Creating minimal Flask app...")
try:
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "test": True})
    
    @app.route('/test')
    def test():
        return jsonify({"message": "Test successful"})
    
    print("✅ Minimal Flask app created successfully")
    print("🚀 Starting test server on port 3032...")
    app.run(host='0.0.0.0', port=3032, debug=False)
    
except Exception as e:
    print(f"❌ Failed to create Flask app: {e}")
    import traceback
    traceback.print_exc()
