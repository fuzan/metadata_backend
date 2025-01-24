from client import Client
from base_service import BaseService
from decorators import routing

class ClientService(BaseService):
    """Service class for handling Client operations."""

    @classmethod
    def initialize_dao(cls, cache_storage):
        """Initialize the Client DAO."""
        super().initialize_dao(cache_storage, 'client', 'clientId')

    @classmethod
    @routing('/api/clients', 'POST')
    def create(cls, data: dict) -> Client:
        """Create a new Client instance."""
        Client.validate_fields(data)
        return super().create(data, Client)

    @classmethod
    @routing('/api/clients/{id}', 'PATCH')
    def update(cls, id: str, data: dict) -> Client:
        """Update an existing Client instance."""
        Client.validate_fields(data)
        return super().update(id, data, Client)

    @classmethod
    @routing('/api/clients/{id}', 'DELETE')
    def delete(cls, id: str) -> None:
        """Delete a Client instance by ID."""
        super().delete(id)

    @classmethod
    @routing('/api/clientsBatch', 'DELETE')
    def delete_batch(cls, data: dict) -> dict:
        """Delete multiple clients by their IDs."""
        client_ids = data.get('clientIds', [])
        return super().delete_batch(client_ids)

    @classmethod
    @routing('/api/clients', 'GET')
    def get_all(cls) -> list:
        """Return all clients."""
        return super().get_all()

    @classmethod
    @routing('/api/clients/{id}', 'GET')
    def get_by_id(cls, id: str) -> dict:
        """Get a single client by ID."""
        return super().get_by_id(id)