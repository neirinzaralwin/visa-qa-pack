from flask import Blueprint, jsonify
from services.database_service import get_db
from utils.logger import logger
from datetime import datetime

bp = Blueprint('health', __name__, url_prefix='/api')

@bp.route('/health', methods=['GET'])
def health_check():
    try:
        # Database check
        db = get_db()
        # Simple database operation to verify connection
        db.collection('_health').document('check').set({'timestamp': datetime.now()})
        db.collection('_health').document('check').delete()
        
        return jsonify({
            "status": "healthy",
            "service": "Visa AI Assistant API",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500