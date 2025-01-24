from typing import Callable, Dict, Tuple
from client_service import ClientService
from services import CacheStorage

class Router:
    """Router class to handle request dispatching."""

    def __init__(self):
        """Initialize router with route mappings."""
        self._routes = {}
        self._register_client_routes()
        self._register_other_routes()

    def _register_client_routes(self):
        """Register all client routes from decorated methods dynamically."""
        registered_routes = {}
        client_service = ClientService()
        client_service.initialize_dao(CacheStorage)
        
        # Scan all methods in ClientService class
        for method_name in dir(ClientService):
            method = getattr(client_service, method_name)
            if hasattr(method, '_route_path') and hasattr(method, '_route_method'):
                route_key = (method._route_path, method._route_method)
                
                # Get required parameters from route info
                required_params = []
                if hasattr(method, '_route_params'):
                    required_params.extend(method._route_params)
                if method._route_method in ['POST', 'PATCH']:
                    required_params.append('data')
                if 'batch' in method._route_path:
                    required_params = ['clientIds']

                registered_routes[route_key] = (method, required_params)

        if not registered_routes:
            raise ValueError("No routes found in ClientService class")

        self._routes.update(registered_routes)

    def _register_other_routes(self):
        """Register non-client routes."""
        other_routes = {
            # TPP routes
            ('/api/tpps', 'GET'): (
                lambda: CacheStorage.get_tpp_data(), 
                []
            ),
            ('/api/tpps/{id}', 'GET'): (
                lambda id: CacheStorage.get_tpp_by_id(id), 
                ['id']
            ),
            # Other routes
            ('/api/scopes', 'GET'): (
                lambda: CacheStorage.get_scope_data(), 
                []
            ),
            ('/api/orgs', 'GET'): (
                lambda: CacheStorage.get_org_data(), 
                []
            ),
            ('/api/tpp_orgs', 'GET'): (
                lambda: CacheStorage.get_tpp_org_data(), 
                []
            ),
            ('/api/environment', 'GET'): (
                lambda: CacheStorage.get_env_data(), 
                []
            )
        }
        self._routes.update(other_routes)

    def extract_path_params(self, route_path: str, actual_path: str) -> tuple[bool, dict]:
        """
        Extract path parameters from actual path based on route pattern.
        
        Example:
        route_path: '/api/clients/{id}/details/{type}'
        actual_path: '/api/clients/123/details/basic'
        returns: (True, {'id': '123', 'type': 'basic'})
        """
        # Split paths into segments
        route_segments = route_path.split('/')
        path_segments = actual_path.split('/')

        # Check if segment counts match
        if len(route_segments) != len(path_segments):
            return False, {}

        # Extract parameters
        params = {}
        for route_seg, path_seg in zip(route_segments, path_segments):
            # Check if segment is a parameter
            if route_seg.startswith('{') and route_seg.endswith('}'):
                param_name = route_seg[1:-1]  # Remove { and }
                params[param_name] = path_seg
            # Check if non-parameter segments match
            elif route_seg != path_seg:
                return False, {}

        return True, params

    def dispatch(self, path: str, method: str, **kwargs) -> dict:
        """
        Dispatch the request to the appropriate handler.
        
        Args:
            path: The request path
            method: The HTTP method
            **kwargs: Additional parameters (data, id, etc.)
            
        Returns:
            dict: The response data
            
        Raises:
            ValueError: If route not found or invalid parameters
        """
        # Find matching route
        route_match = None
        route_params = {}

        for (route_path, route_method), (handler, required_params) in self._routes.items():
            if method != route_method:
                continue

            # Check if route matches and extract parameters
            matches, params = self.extract_path_params(route_path, path)
            if matches:
                route_match = (route_path, route_method)
                route_params = params
                break

        if not route_match:
            raise ValueError(f"Route not found: {method} {path}")

        handler, required_params = self._routes[route_match]

        # Validate and collect parameters
        handler_params = {}
        for param in required_params:
            if param in route_params:
                handler_params[param] = route_params[param]
            elif param == 'data':
                if 'data' not in kwargs:
                    raise ValueError("Request body required")
                handler_params['data'] = kwargs['data']
            elif param == 'clientIds':
                if 'data' not in kwargs or 'clientIds' not in kwargs['data']:
                    raise ValueError("clientIds required in request body")
                handler_params['client_ids'] = kwargs['data']['clientIds']
            else:
                raise ValueError(f"Missing required parameter: {param}")

        # Call handler with collected parameters
        return handler(**handler_params)
