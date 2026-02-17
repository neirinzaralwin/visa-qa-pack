import google.generativeai as genai
import firebase_admin
from firebase_admin import firestore
from config import Config
from utils.logger import logger
from services.database_service import get_prompts_collection
import json

def init_visa_ai_service():
    try:
        if not Config.GOOGLE_AI_API_KEY:
            raise ValueError("GOOGLE_AI_API_KEY not found in environment variables")
        
        genai.configure(api_key=Config.GOOGLE_AI_API_KEY)
        logger.info(f"Google AI Studio initialized with model: {Config.GOOGLE_AI_MODEL}")
        
        # Initialize default prompt if it doesn't exist
        _initialize_default_prompt()
        
    except Exception as e:
        logger.error(f"Failed to initialize Visa AI service: {str(e)}")
        raise

def _initialize_default_prompt():
    """Initialize the default AI assistant prompt in Firestore"""
    try:
        prompts_collection = get_prompts_collection()
        doc_ref = prompts_collection.document('visa_assistant_prompt')
        
        if not doc_ref.get().exists:
            default_prompt = """You are a friendly and professional visa consultant specializing in Thai DTV (Destination Thailand Visa) applications. Your role is to help customers with their visa questions in a natural, human-like way.

Key guidelines:
- Be conversational and friendly, not robotic
- Use casual language similar to the sample conversations
- Ask relevant follow-up questions when needed
- Provide accurate information about DTV visa requirements
- Be helpful and encouraging throughout the process
- Use emojis occasionally to maintain a friendly tone 😊

When responding to customer inquiries:
1. Acknowledge their situation
2. Provide clear, accurate information
3. Ask relevant questions to better assist them
4. Maintain a professional yet friendly tone

Always respond in JSON format: {"reply": "your response here"}"""
            
            doc_ref.set({
                'prompt': default_prompt,
                'updated_at': firestore.SERVER_TIMESTAMP,
                'version': 1
            })
            logger.info("Default visa assistant prompt initialized")
    
    except Exception as e:
        logger.error(f"Failed to initialize default prompt: {str(e)}")

def get_current_prompt():
    """Get the current AI assistant prompt from Firestore"""
    try:
        prompts_collection = get_prompts_collection()
        doc_ref = prompts_collection.document('visa_assistant_prompt')
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict().get('prompt', '')
        else:
            logger.warning("No prompt found in database, using default")
            _initialize_default_prompt()
            return get_current_prompt()
    
    except Exception as e:
        logger.error(f"Failed to get current prompt: {str(e)}")
        raise

def update_prompt(new_prompt):
    """Update the AI assistant prompt in Firestore"""
    try:
        prompts_collection = get_prompts_collection()
        doc_ref = prompts_collection.document('visa_assistant_prompt')
        
        # Get current version and increment
        doc = doc_ref.get()
        current_version = doc.to_dict().get('version', 0) if doc.exists else 0
        
        doc_ref.set({
            'prompt': new_prompt,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'version': current_version + 1
        })
        
        logger.info("AI assistant prompt updated successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to update prompt: {str(e)}")
        return False

def generate_ai_reply(client_sequence, chat_history=None):
    """Generate AI reply based on client sequence and chat history"""
    try:
        # Get current prompt
        current_prompt = get_current_prompt()
        
        # Build conversation context
        conversation_context = ""
        if chat_history:
            conversation_context = "\n\nPrevious conversation:\n"
            for msg in chat_history:
                role = "CLIENT" if msg.get('role') == 'client' else "CONSULTANT"
                conversation_context += f"{role}: {msg.get('message', '')}\n"
        
        # Build the full prompt for the AI
        full_prompt = f"""{current_prompt}

Client message: {client_sequence}
{conversation_context}

Generate your response:"""
        
        # Generate response using Google AI
        model = genai.GenerativeModel(Config.GOOGLE_AI_MODEL)
        response = model.generate_content(full_prompt)
        
        # Parse the response to extract JSON
        response_text = response.text.strip()
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            if '{' in response_text and '}' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                parsed_response = json.loads(json_str)
                ai_reply = parsed_response.get('reply', response_text)
            else:
                ai_reply = response_text
        except json.JSONDecodeError:
            ai_reply = response_text
        
        logger.info(f"Generated AI reply for client sequence")
        return ai_reply
    
    except Exception as e:
        logger.error(f"Failed to generate AI reply: {str(e)}")
        return "I'm sorry, I'm having trouble responding right now. Please try again later."

def improve_ai_prompt(client_sequence, chat_history, consultant_reply, predicted_reply):
    """Improve the AI prompt by comparing predicted vs actual consultant reply"""
    try:
        improvement_prompt = f"""You are an AI prompt engineer. Your task is to improve an AI assistant prompt for visa consulting.

Current AI assistant prompt is working, but we need to make it better based on real consultant responses.

CLIENT MESSAGE: {client_sequence}

CHAT HISTORY:
{json.dumps(chat_history, indent=2) if chat_history else "None"}

PREDICTED AI REPLY: {predicted_reply}

ACTUAL CONSULTANT REPLY: {consultant_reply}

Analyze the differences between the predicted AI reply and the actual consultant reply. Identify what the consultant did better (tone, information, questions asked, etc.) and improve the AI assistant prompt to be more like the consultant.

Return the improved prompt in JSON format: {{"prompt": "improved prompt here"}}"""

        model = genai.GenerativeModel(Config.GOOGLE_AI_MODEL)
        response = model.generate_content(improvement_prompt)
        
        # Parse the improvement response
        response_text = response.text.strip()
        try:
            if '{' in response_text and '}' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                parsed_response = json.loads(json_str)
                improved_prompt = parsed_response.get('prompt', current_prompt)
            else:
                improved_prompt = response_text
        except json.JSONDecodeError:
            improved_prompt = response_text
        
        # Update the prompt in database
        if update_prompt(improved_prompt):
            logger.info("AI prompt improved and updated successfully")
            return improved_prompt
        else:
            logger.error("Failed to update improved prompt")
            return None
    
    except Exception as e:
        logger.error(f"Failed to improve AI prompt: {str(e)}")
        return None

def manually_update_prompt(instructions):
    """Manually update the AI prompt based on specific instructions"""
    try:
        current_prompt = get_current_prompt()
        
        manual_update_prompt = f"""You are an AI prompt engineer. Update the following AI assistant prompt based on the given instructions.

CURRENT PROMPT:
{current_prompt}

UPDATE INSTRUCTIONS:
{instructions}

Return the updated prompt in JSON format: {{"prompt": "updated prompt here"}}"""

        model = genai.GenerativeModel(Config.GOOGLE_AI_MODEL)
        response = model.generate_content(manual_update_prompt)
        
        # Parse the response
        response_text = response.text.strip()
        try:
            if '{' in response_text and '}' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                parsed_response = json.loads(json_str)
                updated_prompt = parsed_response.get('prompt', current_prompt)
            else:
                updated_prompt = response_text
        except json.JSONDecodeError:
            updated_prompt = response_text
        
        # Update the prompt in database
        if update_prompt(updated_prompt):
            logger.info("AI prompt manually updated successfully")
            return updated_prompt
        else:
            logger.error("Failed to update manual prompt")
            return None
    
    except Exception as e:
        logger.error(f"Failed to manually update prompt: {str(e)}")
        return None
