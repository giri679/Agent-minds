"""
Mock API Server for AI Education Agent
Simple server to provide basic API responses for demo purposes
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse

class MockAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        # Root endpoint - health check
        if parsed_path.path == '/':
            response = {
                "status": "online",
                "message": "AI Education Agent API is running",
                "version": "1.0.0",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        
        # Student profile endpoint
        elif parsed_path.path.startswith('/student/'):
            response = {
                "student_id": "STU001",
                "name": "Priya Sharma",
                "grade": 8,
                "school_id": "GOV001",
                "performance": {
                    "Mathematics": 85,
                    "Science": 78,
                    "English": 65,
                    "History": 72
                },
                "learning_style": "Visual",
                "strengths": ["Mathematics", "Science"],
                "focus_areas": ["English Grammar", "History"]
            }
        
        # AI chat endpoint
        elif parsed_path.path == '/ai/chat':
            response = {
                "response": "Hello! I'm your AI tutor. I can help you with any subject. What would you like to learn about today?",
                "confidence": 0.95,
                "suggestions": [
                    "Ask me about Mathematics concepts",
                    "Get help with Science experiments", 
                    "Practice English grammar",
                    "Learn about Historical events"
                ]
            }
        
        # Worksheet generation endpoint
        elif parsed_path.path == '/ai/worksheet':
            response = {
                "worksheet_id": "WS001",
                "subject": "Mathematics",
                "topic": "Algebra",
                "difficulty": "medium",
                "questions": [
                    {
                        "id": 1,
                        "question": "Solve for x: 2x + 5 = 13",
                        "type": "equation",
                        "points": 5
                    },
                    {
                        "id": 2, 
                        "question": "If y = 3x - 2, find y when x = 4",
                        "type": "substitution",
                        "points": 5
                    }
                ],
                "estimated_time": "15 minutes"
            }
        
        # Default response
        else:
            response = {
                "error": "Endpoint not found",
                "available_endpoints": [
                    "/",
                    "/student/{id}",
                    "/ai/chat",
                    "/ai/worksheet"
                ]
            }
        
        # Send JSON response
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        # Handle POST requests
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        # Parse JSON data
        try:
            data = json.loads(post_data.decode())
        except:
            data = {}
        
        # Mock response for POST requests
        response = {
            "status": "success",
            "message": "Data received successfully",
            "received_data": data,
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Custom logging
        print(f"[API] {format % args}")

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MockAPIHandler)
    print("🚀 Mock AI Education Agent API Server starting...")
    print("📡 Server running at: http://localhost:8000")
    print("🔗 Health check: http://localhost:8000/")
    print("📚 Available endpoints:")
    print("   GET  /                 - Health check")
    print("   GET  /student/{id}     - Student profile")
    print("   POST /ai/chat          - AI chat")
    print("   POST /ai/worksheet     - Generate worksheet")
    print("\n✅ Server is ready! The frontend should now show 'AI Connected' status.")
    print("Press Ctrl+C to stop the server.\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
