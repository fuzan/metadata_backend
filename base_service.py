from data_access import DaoImplementation

class BaseService:
    """Base service class for handling common operations."""

    @classmethod
    def initialize_dao(cls, cache_storage, cache_type, id_field):
        """Initialize the DAO."""
        cls._dao = DaoImplementation(cache_storage, cache_type, id_field)

    @classmethod
    def create(cls, data: dict, entity_class) -> object:
        """Create a new entity instance."""
        entity = entity_class.from_dict(data)
        cls._dao.create(entity.to_dict())
        return entity

    @classmethod
    def update(cls, entity_id: str, data: dict, entity_class) -> object:
        """Update an existing entity instance."""
        existing_entity = cls.get_by_id(entity_id)
        updated_data = {**existing_entity, **data}
        updated_entity = entity_class.from_dict(updated_data)
        cls._dao.update(entity_id, updated_entity.to_dict())
        return updated_entity

    @classmethod
    def delete(cls, id: str) -> None:
        """Delete an entity instance by ID."""
        cls._dao.delete_by_id(id)

    @classmethod
    def delete_batch(cls, ids: list) -> dict:
        """Delete multiple entities by their IDs."""
        if not isinstance(ids, list):
            raise ValueError("ids must be a list")
        if not all(isinstance(id, str) for id in ids):
            raise TypeError("All IDs must be strings")
        
        return cls._dao.delete_batch(ids)

    @classmethod
    def get_all(cls) -> list:
        """Return all entities."""
        return cls._dao.get_batch()

    @classmethod
    def get_by_id(cls, id: str) -> dict:
        """Get a single entity by ID."""
        return cls._dao.get_by_id(id)
