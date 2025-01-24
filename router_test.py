import unittest
from unittest.mock import MagicMock
from router import Router
from services import CacheStorage

class TestRouter(unittest.TestCase):
    """Test cases for Router class."""

    def setUp(self):
        """Set up test environment before each test."""
        self.router = Router()
        self.mock_cache = MagicMock()

    def test_path_parameter_extraction(self):
        """Test path parameter extraction functionality."""
        test_cases = [
            # (route_path, actual_path, expected_match, expected_params)
            ('/api/clients', '/api/clients', True, {}),
            ('/api/clients/{id}', '/api/clients/123', True, {'id': '123'}),
            ('/api/{resource}/{id}', '/api/users/456', True, {'resource': 'users', 'id': '456'}),
            ('/api/clients/{id}/details', '/api/clients/123/details', True, {'id': '123'}),
            ('/api/clients/{id}', '/api/users/123', False, {}),
            ('/api/clients', '/api/clients/extra', False, {}),
        ]

        for route_path, actual_path, exp_match, exp_params in test_cases:
            with self.subTest(route=route_path, path=actual_path):
                matches, params = self.router.extract_path_params(route_path, actual_path)
                self.assertEqual(matches, exp_match)
                self.assertEqual(params, exp_params)

    def test_dispatch_get_requests(self):
        """Test dispatching GET requests."""
        test_cases = [
            ('/api/clients', [], list),
            ('/api/clients/1', None, dict),
            ('/api/tpps', [], list),
            ('/api/scopes', [], list),
            ('/api/environment', [], list),
        ]

        for path, _, expected_type in test_cases:
            with self.subTest(path=path):
                result = self.router.dispatch(path, 'GET')
                self.assertIsInstance(result, expected_type)

    def test_dispatch_post_requests(self):
        """Test dispatching POST requests."""
        client_data = {
            'clientId': 'test123',
            'clientName': 'Test Client',
            'clientDesc': 'Test Description',
            'tppId': 'TPP1',
            'clientSecret': 'secret123',
            'logoUri': 'http://example.com/logo.png',
            'uri': 'http://example.com',
            'contacts': ['test@example.com']
        }

        result = self.router.dispatch('/api/clients', 'POST', data=client_data)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['data']['clientId'], 'test123')

    def test_dispatch_patch_requests(self):
        """Test dispatching PATCH requests."""
        update_data = {
            'clientId': '1',
            'clientName': 'Updated Name',
            'clientDesc': 'Updated Description',
            'tppId': 'TPP1',
            'clientSecret': 'secret123',
            'logoUri': 'http://example.com/logo.png',
            'uri': 'http://example.com',
            'contacts': ['test@example.com']
        }

        result = self.router.dispatch('/api/clients/1', 'PATCH', data=update_data)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['data']['clientName'], 'Updated Name')

    def test_dispatch_delete_requests(self):
        """Test dispatching DELETE requests."""
        # Test single delete
        result = self.router.dispatch('/api/clients/1', 'DELETE')
        self.assertEqual(result['status'], 'success')

        # Test batch delete
        result = self.router.dispatch('/api/clients/batch', 'DELETE', 
                                    data={'clientIds': ['2', '3']})
        self.assertEqual(result['status'], 'success')

    def test_dispatch_errors(self):
        """Test error handling in dispatch."""
        error_cases = [
            # (path, method, kwargs, expected_error)
            ('/invalid/path', 'GET', {}, 'Route not found'),
            ('/api/clients', 'INVALID', {}, 'Route not found'),
            ('/api/clients', 'POST', {}, 'Request body required'),
            ('/api/clients/batch', 'DELETE', {'data': {}}, 'clientIds required'),
        ]

        for path, method, kwargs, error_msg in error_cases:
            with self.subTest(path=path, method=method):
                with self.assertRaises(ValueError) as context:
                    self.router.dispatch(path, method, **kwargs)
                self.assertIn(error_msg, str(context.exception))

    def test_route_parameter_validation(self):
        """Test parameter validation in routes."""
        test_cases = [
            # (path, method, data, expected_error)
            ('/api/clients/{id}', 'PATCH', {}, 'Request body required'),
            ('/api/clients/batch', 'DELETE', {'data': {'wrong': []}}, 'clientIds required'),
        ]

        for path, method, kwargs, error_msg in test_cases:
            with self.subTest(path=path, method=method):
                with self.assertRaises(ValueError) as context:
                    self.router.dispatch(path, method, **kwargs)
                self.assertIn(error_msg, str(context.exception))

if __name__ == '__main__':
    unittest.main()