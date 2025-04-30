from entities.client_org import ClientOrg
from services.base_service import BaseService
from decorators import routing

class ClientOrgService(BaseService):
    """Service class for handling Client-Organization operations."""

    @classmethod
    def initialize_dao(cls, cache_storage):
        """Initialize the Client-Organization DAO."""
        super().initialize_dao(cache_storage, 'clientOrg', 'clientOrgId')

    @classmethod
    @routing('/api/client_orgs', 'POST')
    def create(cls, data: dict) -> ClientOrg:
        """Create a new Client-Organization instance."""
        return super().create(data, ClientOrg)

    @classmethod
    @routing('/api/client_orgs/{id}', 'PATCH')
    def update(cls, id: str, data: dict) -> ClientOrg:
        """Update an existing Client-Organization instance."""
        return super().update(id, data, ClientOrg)

    @classmethod
    @routing('/api/client_orgs/{id}', 'DELETE')
    def delete(cls, id: str) -> None:
        """Delete a Client-Organization instance by ID."""
        super().delete(id)

    @classmethod
    @routing('/api/client_orgsBatch', 'DELETE')
    def delete_batch(cls, data: dict) -> dict:
        """Delete multiple Client-Organizations by their IDs."""
        client_org_ids = data.get('clientOrgIds', [])
        return super().delete_batch(client_org_ids)

    @classmethod
    @routing('/api/client_orgs', 'GET')
    def get_all(cls) -> list:
        """Return all Client-Organizations."""
        return super().get_all()

    @classmethod
    @routing('/api/client_orgs/{id}', 'GET')
    def get_by_id(cls, id: str) -> dict:
        """Get a single Client-Organization by ID."""
        return super().get_by_id(id)
