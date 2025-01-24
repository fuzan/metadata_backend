import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from router import Router

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """A simple HTTP request handler with GET and POST functionality."""
    
    def __init__(self, *args, **kwargs):
        self.router = Router()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        try:
            response_data = self.router.dispatch(self.path, 'GET')
            self.attach_headers(response_data)
        except ValueError as e:
            self.send_error(404, str(e))
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")

    def do_POST(self):
        """Handle POST requests."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            response_data = self.router.dispatch(self.path, 'POST', data=data)
            self.attach_headers(response_data)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON format")
        except ValueError as e:
            self.send_error(400, str(e))
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")

    def do_PATCH(self):
        """Handle PATCH requests."""
        try:
            content_length = int(self.headers['Content-Length'])
            patch_data = self.rfile.read(content_length)
            data = json.loads(patch_data.decode('utf-8'))
            
            response_data = self.router.dispatch(self.path, 'PATCH', data=data)
            self.attach_headers(response_data)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON format")
        except ValueError as e:
            self.send_error(400, str(e))
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")

    def do_DELETE(self):
        """Handle DELETE requests."""
        try:
            data = None
            if 'Content-Length' in self.headers:
                content_length = int(self.headers['Content-Length'])
                delete_data = self.rfile.read(content_length)
                data = json.loads(delete_data.decode('utf-8'))
            
            response_data = self.router.dispatch(self.path, 'DELETE', data=data)
            self.attach_headers(response_data)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON format")
        except ValueError as e:
            self.send_error(400, str(e))
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', '0')
        self.add_cors_headers()
        self.end_headers()

    # Utility methods
    def handle_route(self, path, data):
        """Route requests to appropriate handlers."""
        if self.path.startswith(path):
            self.attach_headers(data)
            return True
        return False

    def attach_headers(self, data):
        """Attach headers and send JSON response."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.add_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def add_cors_headers(self):
        """Add CORS headers to the response."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "3600")


def run_server(host='', port=8000):
    """Start the HTTP server."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Serving at {host}:{port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
