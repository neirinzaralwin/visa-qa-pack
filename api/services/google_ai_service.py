import google.generativeai as genai
import json
from typing import List, Dict, Any
from config import Config

class GoogleAIService:
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_AI_API_KEY)
        self.model = genai.GenerativeModel(Config.GOOGLE_AI_MODEL)
    
    def generate_reply(self, client_sequence: str, chat_history: List[Dict[str, str]], prompt: str = None) -> str:
        """Generate AI reply based on client sequence and chat history"""
        
        # Format chat history
        history_text = ""
        for msg in chat_history:
            role = "CONSULTANT" if msg["role"] == "consultant" else "CLIENT"
            history_text += f"- ({role}) {msg['message']}\n"
        
        # Use the provided prompt or fall back to default
        if prompt:
            # Replace placeholders in the custom prompt
            formatted_prompt = prompt.replace("{client_sequence}", client_sequence).replace("{chat_history}", history_text)
            print(f"Using custom prompt from Firestore: {prompt[:100]}...")
        else:
            # Use the default hardcoded prompt
            formatted_prompt = f"""You are a visa consultant specializing in Thai DTV visas. Your responses should be:
- Human and casual, not robotic
- Helpful and informative
- Concise but thorough
- Friendly and approachable

Based on the client's message and chat history, provide an appropriate response in JSON format:
{{"reply": "your response here"}}

Client message: {client_sequence}

Chat history:
{history_text}"""
            print("Using default hardcoded prompt")
        
        try:
            response = self.model.generate_content(formatted_prompt)
            response_text = response.text.strip()
            print(f"Raw AI response: {response_text}")
            
            # Try to extract JSON from the response
            try:
                # Look for JSON pattern in the response
                import re
                json_match = re.search(r'\{[^}]*"reply"[^}]*\}', response_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return result.get("reply", response_text)
                else:
                    # Try parsing the entire response as JSON
                    result = json.loads(response_text)
                    return result.get("reply", response_text)
            except json.JSONDecodeError as je:
                print(f"JSON parsing error: {je}")
                # If JSON parsing fails, return the raw response
                return response_text
                
        except Exception as e:
            print(f"Error generating reply: {e}")
            import traceback
            traceback.print_exc()
            return "I apologize, but I'm having trouble generating a response right now."
    
    def improve_prompt(self, current_prompt: str, client_sequence: str, chat_history: List[Dict[str, str]], 
                      consultant_reply: str, predicted_reply: str) -> str:
        """Improve the AI prompt based on differences between predicted and actual consultant replies"""
        
        editor_prompt = f"""You are an AI prompt editor. Your task is to improve an AI chatbot prompt based on the differences between the predicted AI reply and the actual consultant reply.

Current AI prompt:
{current_prompt}

Client message: {client_sequence}

Chat history:
{self._format_history(chat_history)}

Actual consultant reply: {consultant_reply}
Predicted AI reply: {predicted_reply}

Analyze the differences between the actual and predicted replies. Identify what the consultant did better or differently. Update the AI prompt to make it more aligned with the consultant's style and accuracy. Make surgical, targeted improvements.

Return the updated prompt in JSON format:
{{"prompt": "updated prompt here"}}"""
        
        try:
            response = self.model.generate_content(editor_prompt)
            result = json.loads(response.text.strip())
            return result.get("prompt", current_prompt)
        except Exception as e:
            print(f"Error improving prompt: {e}")
            return current_prompt
    
    def manual_improve_prompt(self, current_prompt: str, instructions: str) -> str:
        """Manually improve the prompt based on specific instructions"""
        
        improvement_prompt = f"""You are an AI prompt editor. Your task is to improve an AI chatbot prompt based on specific instructions.

Current AI prompt:
{current_prompt}

Improvement instructions: {instructions}

Update the prompt according to the instructions while maintaining its core purpose and structure.

Return the updated prompt in JSON format:
{{"prompt": "updated prompt here"}}"""
        
        try:
            response = self.model.generate_content(improvement_prompt)
            result = json.loads(response.text.strip())
            return result.get("prompt", current_prompt)
        except Exception as e:
            print(f"Error manually improving prompt: {e}")
            return current_prompt
    
    def _format_history(self, chat_history: List[Dict[str, str]]) -> str:
        """Format chat history for display"""
        history_text = ""
        for msg in chat_history:
            role = "CONSULTANT" if msg["role"] == "consultant" else "CLIENT"
            history_text += f"- ({role}) {msg['message']}\n"
        return history_text
