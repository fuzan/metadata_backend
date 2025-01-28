from entities.tpp import Tpp
from services.base_service import BaseService
from decorators import routing

class TppService(BaseService):
    """Service class for handling TPP operations."""

    @classmethod
    def initialize_dao(cls, cache_storage):
        """Initialize the TPP DAO."""
        super().initialize_dao(cache_storage, 'tpp', 'tppId')

    @classmethod
    @routing('/api/tpps', 'POST')
    def create(cls, data: dict) -> Tpp:
        """Create a new TPP instance."""
        return super().create(data, Tpp)

    @classmethod
    @routing('/api/tpps/{id}', 'PATCH')
    def update(cls, id: str, data: dict) -> Tpp:
        """Update an existing TPP instance."""
        return super().update(id, data, Tpp)

    @classmethod
    @routing('/api/tpps/{id}', 'DELETE')
    def delete(cls, id: str) -> None:
        """Delete a TPP instance by ID."""
        super().delete(id)

    @classmethod
    @routing('/api/tppsBatch', 'DELETE')
    def delete_batch(cls, data: dict) -> dict:
        """Delete multiple TPPs by their IDs."""
        tpp_ids = data.get('tppIds', [])
        return super().delete_batch(tpp_ids)

    @classmethod
    @routing('/api/tpps', 'GET')
    def get_all(cls) -> list:
        """Return all TPPs."""
        return super().get_all()

    @classmethod
    @routing('/api/tpps/{id}', 'GET')
    def get_by_id(cls, id: str) -> dict:
        """Get a single TPP by ID."""
        return super().get_by_id(id)
