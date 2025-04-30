from entities.tpp_org import TppOrg
from services.base_service import BaseService
from decorators import routing

class TppOrgService(BaseService):
    """Service class for handling TPP-Organization operations."""

    @classmethod
    def initialize_dao(cls, cache_storage):
        """Initialize the TPP-Organization DAO."""
        super().initialize_dao(cache_storage, 'tppOrg', 'tppOrgId')

    @classmethod
    @routing('/api/tpp_orgs', 'POST')
    def create(cls, data: dict) -> TppOrg:
        """Create a new TPP-Organization instance."""
        return super().create(data, TppOrg)

    @classmethod
    @routing('/api/tpp_orgs/{id}', 'PATCH')
    def update(cls, id: str, data: dict) -> TppOrg:
        """Update an existing TPP-Organization instance."""
        return super().update(id, data, TppOrg)

    @classmethod
    @routing('/api/tpp_orgs/{id}', 'DELETE')
    def delete(cls, id: str) -> None:
        """Delete a TPP-Organization instance by ID."""
        super().delete(id)

    @classmethod
    @routing('/api/tpp_orgsBatch', 'DELETE')
    def delete_batch(cls, data: dict) -> dict:
        """Delete multiple TPP-Organizations by their IDs."""
        tpp_org_ids = data.get('tppOrgIds', [])
        return super().delete_batch(tpp_org_ids)

    @classmethod
    @routing('/api/tpp_orgs', 'GET')
    def get_all(cls) -> list:
        """Return all TPP-Organizations."""
        return super().get_all()

    @classmethod
    @routing('/api/tpp_orgs/{id}', 'GET')
    def get_by_id(cls, id: str) -> dict:
        """Get a single TPP-Organization by ID."""
        return super().get_by_id(id)
