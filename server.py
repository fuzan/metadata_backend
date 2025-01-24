import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from concurrent.futures import ThreadPoolExecutor
from router import Router

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """A simple HTTP request handler with GET and POST functionality."""
    
    def __init__(self, *args, **kwargs):
        self.router = Router()
        super().__init__(*args, **kwargs)

    def handle_request(self, method):
        """Handle HTTP requests."""
        try:
            data = None
            if method in ['POST', 'PATCH', 'DELETE']:
                content_length = self.headers.get('Content-Length')
                if content_length:
                    content_length = int(content_length)
                    request_data = self.rfile.read(content_length)
                    data = json.loads(request_data.decode('utf-8'))
            
            response_data = self.router.dispatch(self.path, method, data=data)
            self.attach_headers(response_data)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON format")
        except ValueError as e:
            self.send_error(400 if method != 'GET' else 404, str(e))
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")

    def do_GET(self):
        """Handle GET requests."""
        self.handle_request('GET')

    def do_POST(self):
        """Handle POST requests."""
        self.handle_request('POST')

    def do_PATCH(self):
        """Handle PATCH requests."""
        self.handle_request('PATCH')

    def do_DELETE(self):
        """Handle DELETE requests."""
        self.handle_request('DELETE')

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', '0')
        self.add_cors_headers()
        self.end_headers()

    def attach_headers(self, data):
        """Attach headers and send JSON response."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.add_cors_headers()
        self.end_headers()
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        self.wfile.write(json.dumps(data).encode())

    def add_cors_headers(self):
        """Add CORS headers to the response."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "3600")


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        self.executor = ThreadPoolExecutor(max_workers=10)  # Adjust the number of workers as needed

    def process_request(self, request, client_address):
        """Start a new thread to process the request."""
        self.executor.submit(self.process_request_thread, request, client_address)


def run_server(host='', port=8000):
    """Start the HTTP server."""
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Serving at {host}:{port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
