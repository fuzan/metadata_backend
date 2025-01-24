from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any

T = TypeVar('T')  # Generic type for the entity

class Dao(ABC, Generic[T]):
    """Abstract base class for Data Access Objects."""

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[T]:
        """
        Retrieve an entity by its ID.
        
        Args:
            id: The entity's identifier
            
        Returns:
            The entity if found, None otherwise
        """
        pass

    @abstractmethod
    def get_batch(self, filter_params: Dict[str, Any] = None) -> List[T]:
        """
        Retrieve multiple entities, optionally filtered.
        
        Args:
            filter_params: Optional dictionary of filter parameters
            
        Returns:
            List of entities matching the criteria
        """
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Create a new entity.
        
        Args:
            entity: The entity to create
            
        Returns:
            The created entity with any system-generated fields
            
        Raises:
            ValueError: If entity is invalid
        """
        pass

    @abstractmethod
    def update(self, id: str, entity: T) -> Optional[T]:
        """
        Update an existing entity.
        
        Args:
            id: The entity's identifier
            entity: The entity with updated values
            
        Returns:
            The updated entity if successful, None if entity not found
            
        Raises:
            ValueError: If entity is invalid
        """
        pass

    @abstractmethod
    def delete_by_id(self, id: str) -> bool:
        """
        Delete an entity by its ID.
        
        Args:
            id: The entity's identifier
            
        Returns:
            True if entity was deleted, False if not found
        """
        pass

    @abstractmethod
    def delete_batch(self, ids: List[str]) -> Dict[str, List[str]]:
        """
        Delete multiple entities by their IDs.
        
        Args:
            ids: List of entity identifiers to delete
            
        Returns:
            Dictionary containing lists of successfully and failed deletions
        """
        pass

class DaoImplementation(Dao[T]):
    """Implementation of Data Access Object for any entity type."""

    def __init__(self, cache_storage, cache_type: str, id_field: str = 'id'):
        """
        Initialize DAO with cache storage settings.
        
        Args:
            cache_storage: The cache storage instance
            cache_type: The type of entity in cache (e.g., 'client', 'tpp')
            id_field: The field name used as identifier (default: 'id')
        """
        self.cache_storage = cache_storage
        self.cache_type = cache_type
        self.id_field = id_field

    def get_by_id(self, id: str) -> Optional[T]:
        """Retrieve an entity by its ID."""
        items = self.get_batch()
        return next((item for item in items if item[self.id_field] == id), None)

    def get_batch(self, filter_params: Dict[str, Any] = None) -> List[T]:
        """Retrieve multiple entities, optionally filtered."""
        if not self.cache_storage._cache_initialized:
            self.cache_storage.initialize_cache()
            
        items = self.cache_storage._cache[self.cache_type]
        
        if not filter_params:
            return items

        # Apply filters if provided
        filtered_items = items
        for key, value in filter_params.items():
            filtered_items = [item for item in filtered_items if item.get(key) == value]
        
        return filtered_items

    def create(self, entity: T) -> T:
        """Create a new entity."""
        if hasattr(entity, 'to_dict'):
            entity_dict = entity.to_dict()
        else:
            entity_dict = dict(entity)
            
        self.cache_storage.add_to_cache(entity_dict, self.cache_type)
        return entity

    def update(self, id: str, entity: T) -> Optional[T]:
        """Update an existing entity."""
        if hasattr(entity, 'to_dict'):
            entity_dict = entity.to_dict()
        else:
            entity_dict = dict(entity)

        if self.cache_storage.update_cache(id, entity_dict, self.cache_type, self.id_field):
            return entity
        return None

    def delete_by_id(self, id: str) -> bool:
        """Delete an entity by its ID."""
        return self.cache_storage.delete_from_cache(id, self.cache_type, self.id_field)

    def delete_batch(self, ids: List[str]) -> Dict[str, List[str]]:
        """Delete multiple entities by their IDs."""
        success_ids = []
        failed_ids = []
        
        for item_id in ids:
            if self.delete_by_id(item_id):
                success_ids.append(item_id)
            else:
                failed_ids.append(item_id)
                
        return {
            "status": "success" if not failed_ids else "partial",
            "deleted": success_ids,
            "failed": failed_ids,
            "message": f"Successfully deleted {len(success_ids)} items, failed to delete {len(failed_ids)} items"
        }
