from functools import wraps
from typing import List

VALID_METHODS = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'}

def routing(path: str, method: str):
    """
    Decorator to register route handlers.
    
    Args:
        path: URL path pattern (must start with '/')
        method: HTTP method (must be one of VALID_METHODS)
    """
    if not path.startswith('/'):
        raise ValueError("Path must start with '/'")
    if method not in VALID_METHODS:
        raise ValueError(f"Method must be one of: {', '.join(VALID_METHODS)}")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Store routing info and required parameters
        wrapper._route_path = path
        wrapper._route_method = method
        # Extract parameter names from path
        wrapper._route_params = [
            segment[1:-1]  # Remove { and }
            for segment in path.split('/')
            if segment.startswith('{') and segment.endswith('}')
        ]
        return wrapper
    return decorator