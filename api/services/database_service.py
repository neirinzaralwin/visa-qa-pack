import firebase_admin
from firebase_admin import credentials, firestore
from config import Config
from utils.logger import logger

db = None

def init_database():
    global db
    try:
        logger.info("Initializing Firebase Firestore service...")
        
        # Create credentials dictionary from environment variables
        credentials_dict = {
            "type": "service_account",
            "project_id": Config.FIREBASE_PROJECT_ID,
            "private_key_id": Config.FIREBASE_PRIVATE_KEY_ID,
            "private_key": Config.FIREBASE_PRIVATE_KEY,
            "client_email": Config.FIREBASE_CLIENT_EMAIL,
            "client_id": Config.FIREBASE_CLIENT_ID,
            "auth_uri": Config.FIREBASE_AUTH_URI,
            "token_uri": Config.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{Config.FIREBASE_CLIENT_EMAIL}"
        }
        
        # Initialize Firebase Admin with credentials dictionary
        cred = credentials.Certificate(credentials_dict)
        firebase_admin.initialize_app(cred)
        
        # Get Firestore client
        db = firestore.client()
        logger.info("Firebase Firestore connection established")
        
    except Exception as e:
        logger.error(f"Firebase initialization failed: {str(e)}")
        raise