from client import Client
from data_access import DaoImplementation
from decorators import routing

class ClientService:
    """Service class for handling Client operations."""

    @classmethod
    def initialize_dao(cls, cache_storage):
        """Initialize the Client DAO."""
        cls._dao = DaoImplementation(cache_storage, 'client', 'clientId')

    @classmethod
    @routing('/api/clients', 'POST')
    def create(cls, data: dict) -> Client:
        """Create a new Client instance."""
        Client.validate_fields(data)
        client = Client.from_dict(data)
        cls._dao.create(client.to_dict())
        return client

    @classmethod
    @routing('/api/clients/{id}', 'PATCH')
    def update(cls, client_id: str, data: dict) -> Client:
        """Update an existing Client instance."""
        existing_client = cls.get_by_id(client_id)
        updated_data = {**existing_client.to_dict(), **data}
        Client.validate_fields(updated_data)
        updated_client = Client.from_dict(updated_data)
        cls._dao.update(client_id, updated_client.to_dict())
        return updated_client

    @classmethod
    @routing('/api/clients/{id}', 'DELETE')
    def delete(cls, id: str) -> None:
        """Delete a Client instance by ID."""
        cls._dao.delete_by_id(id)

    @classmethod
    @routing('/api/clients/batch', 'DELETE')
    def delete_batch(cls, client_ids: list) -> dict:
        """Delete multiple clients by their IDs."""
        if not isinstance(client_ids, list):
            raise ValueError("client_ids must be a list")
        if not all(isinstance(id, str) for id in client_ids):
            raise TypeError("All client IDs must be strings")
        
        return cls._dao.delete_batch(client_ids)

    @classmethod
    @routing('/api/clients', 'GET')
    def get_all(cls) -> list:
        """Return all clients."""
        return cls._dao.get_batch()

    @classmethod
    @routing('/api/clients/{id}', 'GET')
    def get_by_id(cls, id: str) -> dict:
        """Get a single client by ID."""
        return cls._dao.get_by_id(id)