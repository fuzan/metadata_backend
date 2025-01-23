import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from tpp import Tpp
from scope import Scope
from services import DataFactory


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """A simple HTTP request handler with GET and POST functionality."""

    def handle_client_creation(self, client_data):
        """Handle client creation logic and validation."""
        required_fields = {
            'clientId': str,
            'clientName': str,
            'clientDesc': str,
            'tppId': str,
            'clientSecret': str,
            'logoUri': str,
            'uri': str,
            'contacts': list
        }

        for field, field_type in required_fields.items():
            if field not in client_data:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(client_data[field], field_type):
                raise TypeError(f"Invalid type for {field}: expected {field_type.__name__}")
            if field == 'contacts' and not all(isinstance(x, str) for x in client_data[field]):
                raise TypeError("All contacts must be strings")

        DataFactory.add_to_cache(client_data, 'client')
        return {
            "status": "success",
            "message": "Client created successfully",
            "data": client_data
        }

    def handle_tpp_creation(self, tpp_data):
        """Handle TPP creation logic and validation."""
        required_fields = {
            'tppId': str,
            'tppName': str,
            'tppType': str,
            'verifiedClient': str,
            'scopeNameList': str,
            'tppDesc': str
        }

        for field, field_type in required_fields.items():
            if field not in tpp_data:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(tpp_data[field], field_type):
                raise TypeError(f"Invalid type for {field}: expected {field_type.__name__}")

        tpp = Tpp.from_dict(tpp_data)
        DataFactory.add_to_cache(tpp.to_dict(), 'tpp')
        return {
            "status": "success",
            "message": "TPP created successfully",
            "data": tpp.to_dict()
        }

    def delete_client_by_id(self, client_id):
        """Delete a client by ID."""
        if DataFactory.delete_from_cache(client_id, 'client'):
            return {
                "status": "success",
                "message": f"Client with ID {client_id} successfully deleted"
            }
        return None

    def handle_client_batch_deletion(self, client_ids):
        """Handle batch deletion of clients."""
        if not isinstance(client_ids, list):
            raise ValueError("client_ids must be a list")
        if not all(isinstance(id, str) for id in client_ids):
            raise TypeError("All client IDs must be strings")
        
        return DataFactory.delete_client_batch(client_ids)

    def do_GET(self):
        """Handle GET requests."""
        if self.path.startswith('/api/clients/'):
            client_id = self.path.split('/api/clients/')[-1]
            if client_id:
                client = DataFactory.get_client_by_id(client_id)
                if client:
                    self.attach_headers(client)
                    return
                self.send_error(404, "Client not found")
                return
        elif self.path.startswith('/api/tpps/'):
            tpp_id = self.path.split('/api/tpps/')[-1]
            if tpp_id:
                tpp = DataFactory.get_tpp_by_id(tpp_id)
                if tpp:
                    self.attach_headers(tpp)
                    return
                self.send_error(404, "TPP not found")
                return

        if self.handle_route('/api/clients', DataFactory.get_client_data()):
            return
        elif self.handle_route('/api/tpps', DataFactory.get_tpp_data()):
            return
        elif self.handle_route('/api/scopes', DataFactory.get_scope_data()):
            return
        elif self.handle_route('/api/orgs', DataFactory.get_org_data()):
            return
        elif self.handle_route('/api/tpp_orgs', DataFactory.get_tpp_org_data()):
            return
        elif self.handle_route('/api/environment', DataFactory.get_env_data()):
            return
        self.send_error(404, "Not Found")

    def do_POST(self):
        """Handle POST requests for client and TPP creation."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path.startswith('/api/tpps'):
                response_data = self.handle_tpp_creation(data)
                self.attach_headers(response_data)
                return
            elif self.path.startswith('/api/clients'):
                response_data = self.handle_client_creation(data)
                self.attach_headers(response_data)
                return
            
            self.send_error(404, "Not Found")

        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON format")
        except (ValueError, TypeError) as e:
            self.send_error(400, str(e))
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")

    def do_DELETE(self):
        """Handle DELETE requests."""
        try:
            if self.path == '/api/clients/batch':
                content_length = int(self.headers['Content-Length'])
                delete_data = self.rfile.read(content_length)
                data = json.loads(delete_data.decode('utf-8'))
                
                if 'clientIds' not in data:
                    raise ValueError("Missing clientIds in request body")
                
                result = self.handle_client_batch_deletion(data['clientIds'])
                self.attach_headers(result)
                return
            elif self.path.startswith('/api/clients/'):
                client_id = self.path.split('/api/clients/')[-1]
                if client_id:
                    result = self.delete_client_by_id(client_id)
                    if result:
                        self.attach_headers(result)
                        return
                    self.send_error(404, "Client not found")
                    return
            self.send_error(404, "Not Found")

        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON format")
        except (ValueError, TypeError) as e:
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
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "3600")


def run_server(host='', port=8000):
    """Start the HTTP server."""
    DataFactory.initialize_cache()
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Serving at {host}:{port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
