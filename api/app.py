import os
from flask import Flask
from flask_cors import CORS
from controllers import health_controller, chat_controller
from config import Config

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
    
    from services.database_service import init_database
    
    init_database()
    
    app.register_blueprint(health_controller.bp)
    app.register_blueprint(chat_controller.chat_controller)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=Config.PORT, debug=False)