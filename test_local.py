#!/usr/bin/env python3
import subprocess
import sys
import time
import requests

def test_local():
    print("🧪 Testing local Flask app...")
    
    # Start the app in background
    process = subprocess.Popen([sys.executable, 'app.py'], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
    
    # Wait for app to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        response = requests.get('http://localhost:3032/health', timeout=5)
        print(f"✅ Local health check: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test chat endpoint
        chat_data = {
            "message": "Hello test",
            "session_id": "test_123"
        }
        chat_response = requests.post('http://localhost:3032/api/chat', 
                                 json=chat_data, timeout=5)
        print(f"✅ Local chat test: {chat_response.status_code}")
        print(f"Response: {chat_response.json()}")
        
    except Exception as e:
        print(f"❌ Local test failed: {e}")
    finally:
        process.terminate()
        print("🛑 Local test completed")

if __name__ == "__main__":
    test_local()
