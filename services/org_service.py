from entities.org import Org
from services.base_service import BaseService
from decorators import routing

class OrgService(BaseService):
    """Service class for handling Organization operations."""

    @classmethod
    def initialize_dao(cls, cache_storage):
        """Initialize the Organization DAO."""
        super().initialize_dao(cache_storage, 'org', 'orgId')

    @classmethod
    @routing('/api/orgs', 'POST')
    def create(cls, data: dict) -> Org:
        """Create a new Organization instance."""
        return super().create(data, Org)

    @classmethod
    @routing('/api/orgs/{id}', 'PATCH')
    def update(cls, id: str, data: dict) -> Org:
        """Update an existing Organization instance."""
        return super().update(id, data, Org)

    @classmethod
    @routing('/api/orgs/{id}', 'DELETE')
    def delete(cls, id: str) -> None:
        """Delete an Organization instance by ID."""
        super().delete(id)

    @classmethod
    @routing('/api/orgsBatch', 'DELETE')
    def delete_batch(cls, data: dict) -> dict:
        """Delete multiple organizations by their IDs."""
        org_ids = data.get('orgIds', [])
        return super().delete_batch(org_ids)

    @classmethod
    @routing('/api/orgs', 'GET')
    def get_all(cls) -> list:
        """Return all organizations."""
        return super().get_all()

    @classmethod
    @routing('/api/orgs/{id}', 'GET')
    def get_by_id(cls, id: str) -> dict:
        """Get a single organization by ID."""
        return super().get_by_id(id)
