import re
from services.client_service import ClientService
from services.tpp_service import TppService
from services.org_service import OrgService
from services.client_org_service import ClientOrgService
from services.tpp_org_service import TppOrgService
from cache import CacheStorage

class Router:
    """Router class to handle request dispatching."""

    def __init__(self):
        """Initialize router with route mappings."""
        self._routes = {}
        self._register_client_routes()
        self._register_tpp_routes()
        self._register_org_routes()
        self._register_client_org_routes()
        self._register_tpp_org_routes()
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
                if method._route_method in ['POST', 'PATCH', 'DELETE']:
                    required_params.append('data')
                if 'Batch' in method._route_path:
                    required_params = ['clientIds']

                registered_routes[route_key] = (method, required_params)

        if not registered_routes:
            raise ValueError("No routes found in ClientService class")

        self._routes.update(registered_routes)

    def _register_tpp_routes(self):
        """Register all TPP routes from decorated methods dynamically."""
        registered_routes = {}
        tpp_service = TppService()
        tpp_service.initialize_dao(CacheStorage)
        
        # Scan all methods in TppService class
        for method_name in dir(TppService):
            method = getattr(tpp_service, method_name)
            if hasattr(method, '_route_path') and hasattr(method, '_route_method'):
                route_key = (method._route_path, method._route_method)
                
                # Get required parameters from route info
                required_params = []
                if hasattr(method, '_route_params'):
                    required_params.extend(method._route_params)
                if method._route_method in ['POST', 'PATCH', 'DELETE']:
                    required_params.append('data')
                if 'Batch' in method._route_path:
                    required_params = ['tppIds']

                registered_routes[route_key] = (method, required_params)

        if not registered_routes:
            raise ValueError("No routes found in TppService class")

        self._routes.update(registered_routes)

    def _register_org_routes(self):
        """Register all organization routes from decorated methods dynamically."""
        registered_routes = {}
        org_service = OrgService()
        org_service.initialize_dao(CacheStorage)
        
        # Scan all methods in OrgService class
        for method_name in dir(OrgService):
            method = getattr(org_service, method_name)
            if hasattr(method, '_route_path') and hasattr(method, '_route_method'):
                route_key = (method._route_path, method._route_method)
                
                # Get required parameters from route info
                required_params = []
                if hasattr(method, '_route_params'):
                    required_params.extend(method._route_params)
                if method._route_method in ['POST', 'PATCH', 'DELETE']:
                    required_params.append('data')
                if 'Batch' in method._route_path:
                    required_params = ['orgIds']

                registered_routes[route_key] = (method, required_params)

        if not registered_routes:
            raise ValueError("No routes found in OrgService class")

        self._routes.update(registered_routes)

    def _register_client_org_routes(self):
        """Register all client-organization routes from decorated methods dynamically."""
        registered_routes = {}
        client_org_service = ClientOrgService()
        client_org_service.initialize_dao(CacheStorage)
        
        # Scan all methods in ClientOrgService class
        for method_name in dir(ClientOrgService):
            method = getattr(client_org_service, method_name)
            if hasattr(method, '_route_path') and hasattr(method, '_route_method'):
                route_key = (method._route_path, method._route_method)
                
                # Get required parameters from route info
                required_params = []
                if hasattr(method, '_route_params'):
                    required_params.extend(method._route_params)
                if method._route_method in ['POST', 'PATCH', 'DELETE']:
                    required_params.append('data')
                if 'Batch' in method._route_path:
                    required_params = ['clientOrgIds']

                registered_routes[route_key] = (method, required_params)

        if not registered_routes:
            raise ValueError("No routes found in ClientOrgService class")

        self._routes.update(registered_routes)

    def _register_tpp_org_routes(self):
        """Register all TPP-organization routes from decorated methods dynamically."""
        registered_routes = {}
        tpp_org_service = TppOrgService()
        tpp_org_service.initialize_dao(CacheStorage)
        
        # Scan all methods in TppOrgService class
        for method_name in dir(TppOrgService):
            method = getattr(tpp_org_service, method_name)
            if hasattr(method, '_route_path') and hasattr(method, '_route_method'):
                route_key = (method._route_path, method._route_method)
                
                # Get required parameters from route info
                required_params = []
                if hasattr(method, '_route_params'):
                    required_params.extend(method._route_params)
                if method._route_method in ['POST', 'PATCH', 'DELETE']:
                    required_params.append('data')
                if 'Batch' in method._route_path:
                    required_params = ['tppOrgIds']

                registered_routes[route_key] = (method, required_params)

        if not registered_routes:
            raise ValueError("No routes found in TppOrgService class")

        self._routes.update(registered_routes)

    def _register_other_routes(self):
        """Register non-client routes."""
        other_routes = {
            # Other routes
            ('/api/scopes', 'GET'): (
                lambda: CacheStorage.get_scope_data(), 
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

        # Check if segment counts match or if actual_path is part of route_path
        if len(route_segments) != len(path_segments):
            if actual_path.startswith(route_path):
                return True, {}

        # Extract query parameters from the actual path
        params = {}
        if '?' in actual_path:
            actual_path, query_string = actual_path.split('?', 1)
            query_params = dict(qc.split('=') for qc in query_string.split('&'))
            params.update(query_params)

        # Extract path parameters from the actual path
        path_pattern = re.sub(r'{[^/]+}', r'([^/]+)', route_path)
        match = re.match(path_pattern, actual_path)
        if match:
            path_params = match.groups()
            param_names = [
                segment[1:-1]  # Remove { and }
                for segment in route_segments
                if segment.startswith('{') and segment.endswith('}')
            ]
            for param_name, param_value in zip(param_names, path_params):
                params[param_name] = param_value

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

        for (route_path, route_method), (handler, _) in self._routes.items():
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

        handler = self._routes[route_match][0]

        # Validate and collect parameters
        handler_params = {}
        
        for param in route_params:
            handler_params[param] = route_params[param]
        
        if 'data' in kwargs:
            handler_params['data'] = kwargs['data']

        # Call handler with collected parameters
        return handler(**handler_params)
