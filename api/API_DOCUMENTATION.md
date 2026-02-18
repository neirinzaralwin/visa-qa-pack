# Visa QA Chatbot API Documentation

## Overview
This API provides intelligent visa consultation responses using Google AI Studio. The system is self-learning and can improve its responses over time.

## Base URL
```
http://localhost:3032
```

## Endpoints

### 1. Generate AI Reply
**POST** `/generate-reply`

Generates an AI response based on client message and conversation history.

#### Request Body
```json
{
  "clientSequence": "I'm American and currently in Bali. Can I apply from Indonesia?",
  "chatHistory": [
    {
      "role": "consultant", 
      "message": "Hi there! Thank you for reaching out. The DTV is perfect for remote workers like yourself."
    },
    {
      "role": "client", 
      "message": "Hello, I'm interested in the DTV visa for Thailand."
    }
  ]
}
```

#### Response
```json
{
  "aiReply": "Hey there! Good question. Since you're an American citizen, typically you'd apply for a Thai visa from your home country or a country where you have legal residency..."
}
```

#### Postman Setup
- **Method**: POST
- **URL**: `http://localhost:3032/generate-reply`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: Raw JSON (select "raw" and "JSON" in Postman)

---

### 2. Auto-Improve AI (Self-Learning)
**POST** `/improve-ai`

Automatically improves the AI prompt by comparing predicted vs actual consultant replies.

#### Request Body
```json
{
  "clientSequence": "I'm American and currently in Bali. Can I apply from Indonesia?",
  "chatHistory": [
    {
      "role": "consultant", 
      "message": "Hi there! Thank you for reaching out."
    },
    {
      "role": "client", 
      "message": "Hello, I'm interested in the DTV visa."
    }
  ],
  "consultantReply": "Yes, absolutely! You can apply at the Thai Embassy in Jakarta. I'd recommend scheduling an appointment soon as slots fill up quickly."
}
```

#### Response
```json
{
  "predictedReply": "Hey there! Good question. Since you're an American citizen...",
  "updatedPrompt": "You are a visa consultant specializing in Thai DTV visas..."
}
```

#### Postman Setup
- **Method**: POST
- **URL**: `http://localhost:3032/improve-ai`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: Raw JSON

---

### 3. Manual AI Improvement
**POST** `/improve-ai-manually`

Manually updates the AI prompt with specific instructions.

#### Request Body
```json
{
  "instructions": "Be more concise. Always mention appointment booking proactively. Add more emojis to sound friendly."
}
```

#### Response
```json
{
  "updatedPrompt": "You are a visa consultant specializing in Thai DTV visas. Be more concise and always mention appointment booking proactively. Use emojis to sound friendly..."
}
```

#### Postman Setup
- **Method**: POST
- **URL**: `http://localhost:3032/improve-ai-manually`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: Raw JSON

---

### 4. Health Check
**GET** `/health`

Checks if the API is running.

#### Response
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

## Quick Start Guide for Postman

1. **Create a new collection** called "Visa Chatbot API"

2. **Add the following requests**:

   **Request 1: Generate Reply**
   - Name: "Generate AI Reply"
   - Method: POST
   - URL: `http://localhost:3032/generate-reply`
   - Headers: `Content-Type: application/json`
   - Body: Use the example JSON above

   **Request 2: Auto-Improve**
   - Name: "Auto-Improve AI"
   - Method: POST  
   - URL: `http://localhost:3032/improve-ai`
   - Headers: `Content-Type: application/json`
   - Body: Use the example JSON above

   **Request 3: Manual Improve**
   - Name: "Manual Improve AI"
   - Method: POST
   - URL: `http://localhost:3032/improve-ai-manually`
   - Headers: `Content-Type: application/json`
   - Body: Use the example JSON above

3. **Test the API**:
   - Start the server: `python app.py`
   - Send the "Generate AI Reply" request first
   - Try the other endpoints to see the self-learning features

## Environment Setup

Make sure your `.env` file contains:
```
GOOGLE_AI_API_KEY=your_google_ai_studio_api_key_here
GOOGLE_AI_MODEL=gemini-1.5-flash
```

## Error Responses

All endpoints return errors in this format:
```json
{
  "error": "Error description"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (missing required fields)
- `500`: Internal Server Error
