import http.server
import socketserver
import json
import os

PORT = 8000
DATA_FILE = 'responses.json'
DB_FILE = 'database.json'

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/database':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            if os.path.exists(DB_FILE):
                with open(DB_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(json.dumps({}).encode())
        elif self.path == '/api/load':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(json.dumps({}).encode())
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api/save':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        elif self.path == '/api/login':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                username = data.get('username')
                password = data.get('password')
                
                # Mock login
                if username and password:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": True, 
                        "username": username, 
                        "token": "fake-jwt-token"
                    }).encode())
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Servidor rodando em http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
