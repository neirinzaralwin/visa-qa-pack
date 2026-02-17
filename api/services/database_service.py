import firebase_admin
from firebase_admin import credentials, firestore
from config import Config
from utils.logger import logger
import os

db = None

def init_database():
    global db
    try:
        logger.info("Initializing Firebase Firestore service...")
        
        # Check if all required Firebase credentials are available
        required_vars = [
            Config.FIREBASE_PROJECT_ID,
            Config.FIREBASE_PRIVATE_KEY_ID,
            Config.FIREBASE_PRIVATE_KEY,
            Config.FIREBASE_CLIENT_EMAIL,
            Config.FIREBASE_CLIENT_ID
        ]
        
        if not all(required_vars):
            missing_vars = [var_name for var_name, var_value in [
                ("FIREBASE_PROJECT_ID", Config.FIREBASE_PROJECT_ID),
                ("FIREBASE_PRIVATE_KEY_ID", Config.FIREBASE_PRIVATE_KEY_ID),
                ("FIREBASE_PRIVATE_KEY", Config.FIREBASE_PRIVATE_KEY),
                ("FIREBASE_CLIENT_EMAIL", Config.FIREBASE_CLIENT_EMAIL),
                ("FIREBASE_CLIENT_ID", Config.FIREBASE_CLIENT_ID)
            ] if not var_value]
            raise ValueError(f"Missing Firebase credentials: {', '.join(missing_vars)}")
        
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

def get_db():
    if db is None:
        raise RuntimeError("Database not initialized")
    return db

# Collection helpers
def get_prompts_collection():
    return get_db().collection('ai_prompts')

def get_conversations_collection():
    return get_db().collection('conversations')

def get_training_data_collection():
    return get_db().collection('training_data')