from flask import Blueprint, request, jsonify
from services.google_ai_service import GoogleAIService
from services.database_service import get_prompt, update_prompt

chat_controller = Blueprint('chat', __name__)
ai_service = GoogleAIService()

@chat_controller.route('/generate-reply', methods=['POST'])
def generate_reply():
    """Generate an AI response based on conversation context"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'clientSequence' not in data:
            return jsonify({'error': 'clientSequence is required'}), 400
        
        client_sequence = data['clientSequence']
        chat_history = data.get('chatHistory', [])
        
        # Get current prompt from database
        current_prompt = get_prompt()
        
        # Generate AI reply
        ai_reply = ai_service.generate_reply(client_sequence, chat_history, current_prompt)
        
        return jsonify({
            'aiReply': ai_reply
        })
        
    except Exception as e:
        import traceback
        print(f"Controller error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@chat_controller.route('/improve-ai', methods=['POST'])
def improve_ai():
    """Auto-improve the AI prompt by comparing predicted vs actual consultant reply"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['clientSequence', 'chatHistory', 'consultantReply']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields: clientSequence, chatHistory, consultantReply'}), 400
        
        client_sequence = data['clientSequence']
        chat_history = data['chatHistory']
        consultant_reply = data['consultantReply']
        
        # Get current prompt from database
        current_prompt = get_prompt()
        
        # Generate predicted reply
        predicted_reply = ai_service.generate_reply(client_sequence, chat_history, current_prompt)
        
        # Improve the prompt
        updated_prompt = ai_service.improve_prompt(
            current_prompt, client_sequence, chat_history, 
            consultant_reply, predicted_reply
        )
        
        # Update prompt in database
        update_prompt(updated_prompt)
        
        return jsonify({
            'predictedReply': predicted_reply,
            'updatedPrompt': updated_prompt
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_controller.route('/improve-ai-manually', methods=['POST'])
def improve_ai_manually():
    """Manually update the AI prompt with specific instructions"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'instructions' not in data:
            return jsonify({'error': 'instructions is required'}), 400
        
        instructions = data['instructions']
        
        # Get current prompt from database
        current_prompt = get_prompt()
        
        # Improve the prompt
        updated_prompt = ai_service.manual_improve_prompt(current_prompt, instructions)
        
        # Update prompt in database
        update_prompt(updated_prompt)
        
        return jsonify({
            'updatedPrompt': updated_prompt
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
