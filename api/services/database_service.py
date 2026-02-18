import firebase_admin
from firebase_admin import credentials, firestore
from config import Config
from utils.logger import logger
import json
import os

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

        upload_conversation_to_firestore()
        
    except Exception as e:
        logger.error(f"Firebase initialization failed: {str(e)}")
        raise


def upload_conversation_to_firestore():
    """
    Upload conversation data to Firestore if conversations collection doesn't exist.
    Each conversation becomes a document with metadata.
    """
    try:
        global db
        
        # Check if conversations collection already exists
        conversations_ref = db.collection('conversations')
        existing_docs = list(conversations_ref.limit(1).get())
        
        if existing_docs:
            logger.info("Conversations collection already exists. Skipping upload.")
            return
        
        logger.info("Conversations collection not found. Starting upload...")
        
        # Load conversations.json
        conversations_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'conversations.json')
        
        if not os.path.exists(conversations_path):
            logger.error(f"Conversations file not found at: {conversations_path}")
            return
        
        with open(conversations_path, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
        
        logger.info(f"Loaded {len(conversations)} conversations from JSON file")
        
        # Upload each conversation as a document
        for idx, conversation in enumerate(conversations):
            # Prepare conversation data with metadata
            conversation_data = {
                'contact_id': conversation.get('contact_id', f'unknown_{idx}'),
                'scenario': conversation.get('scenario', 'Unknown scenario'),
                'messages': conversation.get('conversation', []),
                'message_count': len(conversation.get('conversation', [])),
                'created_at': firestore.SERVER_TIMESTAMP,
                'processed': False,
                'conversation_index': idx
            }
            
            # Create document with custom ID
            doc_id = f"conv_{conversation.get('contact_id', idx)}"
            doc_ref = conversations_ref.document(doc_id)
            doc_ref.set(conversation_data)
            
            logger.info(f"Uploaded conversation {idx + 1}/{len(conversations)}: {doc_id}")
        
        logger.info(f"✅ Successfully uploaded {len(conversations)} conversations to Firestore")
        
    except Exception as e:
        logger.error(f"Failed to upload conversations to Firestore: {str(e)}")
        raise

def get_prompt():
    """Get the current AI prompt from database"""
    try:
        global db
        if not db:
            init_database()
        
        prompt_ref = db.collection('ai_config').document('chat_prompt')
        doc = prompt_ref.get()
        
        if doc.exists:
            return doc.to_dict().get('prompt', _get_default_prompt())
        else:
            # Create default prompt if it doesn't exist
            default_prompt = _get_default_prompt()
            prompt_ref.set({'prompt': default_prompt})
            return default_prompt
            
    except Exception as e:
        logger.error(f"Failed to get prompt: {str(e)}")
        return _get_default_prompt()

def update_prompt(new_prompt):
    """Update the AI prompt in database"""
    try:
        global db
        if not db:
            init_database()
        
        prompt_ref = db.collection('ai_config').document('chat_prompt')
        prompt_ref.set({'prompt': new_prompt})
        logger.info("AI prompt updated successfully")
        
    except Exception as e:
        logger.error(f"Failed to update prompt: {str(e)}")
        raise

def _get_default_prompt():
    """Get the default AI prompt"""
    return """You are a visa consultant specializing in Thai DTV visas. Your responses should be:
- Human and casual, not robotic
- Helpful and informative
- Concise but thorough
- Friendly and approachable

Based on the client's message and chat history, provide an appropriate response in JSON format:
{{"reply": "your response here"}}

Client message: {client_sequence}

Chat history:
{chat_history}"""
    