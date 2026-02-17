import os
from flask import Flask
from controllers import visa_ai_controller, health_controller

def create_app():
    app = Flask(__name__)
    
    # Initialize services
    from services.database_service import init_database
    from services.visa_ai_service import init_visa_ai_service
    
    init_database()
    init_visa_ai_service()
    
    # Register blueprints
    app.register_blueprint(visa_ai_controller.bp)
    app.register_blueprint(health_controller.bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 3032))
    app.run(host='0.0.0.0', port=port, debug=False)