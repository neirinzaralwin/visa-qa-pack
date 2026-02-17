from flask import Blueprint, request, jsonify
from utils.logger import logger
from services.visa_ai_service import generate_ai_reply, improve_ai_prompt, manually_update_prompt

bp = Blueprint('visa_ai', __name__, url_prefix='/api')

@bp.route('/generate-reply', methods=['POST'])
def generate_reply():
    """Generate an AI response based on conversation context"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        client_sequence = data.get('clientSequence')
        chat_history = data.get('chatHistory', [])
        
        if not client_sequence:
            return jsonify({"error": "clientSequence is required"}), 400
        
        # Generate AI reply
        ai_reply = generate_ai_reply(client_sequence, chat_history)
        
        return jsonify({
            "aiReply": ai_reply
        })
    
    except Exception as e:
        logger.error(f"Error in generate-reply: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/improve-ai', methods=['POST'])
def improve_ai():
    """Auto-improve the AI prompt by comparing predicted vs actual consultant reply"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        client_sequence = data.get('clientSequence')
        chat_history = data.get('chatHistory', [])
        consultant_reply = data.get('consultantReply')
        
        if not client_sequence or not consultant_reply:
            return jsonify({"error": "clientSequence and consultantReply are required"}), 400
        
        # First generate predicted reply
        predicted_reply = generate_ai_reply(client_sequence, chat_history)
        
        # Then improve the prompt
        updated_prompt = improve_ai_prompt(client_sequence, chat_history, consultant_reply, predicted_reply)
        
        if updated_prompt:
            return jsonify({
                "predictedReply": predicted_reply,
                "updatedPrompt": updated_prompt
            })
        else:
            return jsonify({"error": "Failed to improve AI prompt"}), 500
    
    except Exception as e:
        logger.error(f"Error in improve-ai: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/improve-ai-manually', methods=['POST'])
def improve_ai_manually():
    """Manually update the AI prompt with specific instructions"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        instructions = data.get('instructions')
        
        if not instructions:
            return jsonify({"error": "instructions are required"}), 400
        
        # Update the prompt manually
        updated_prompt = manually_update_prompt(instructions)
        
        if updated_prompt:
            return jsonify({
                "updatedPrompt": updated_prompt
            })
        else:
            return jsonify({"error": "Failed to update AI prompt"}), 500
    
    except Exception as e:
        logger.error(f"Error in improve-ai-manually: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
