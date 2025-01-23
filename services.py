from tpp import Tpp
from scope import Scope

class DataFactory:
    """Factory class to manage all data operations."""
    
    _cache = {
        'client': [],
        'tpp': [],
        'scope': []
    }
    _cache_initialized = False

    @classmethod
    def initialize_cache(cls):
        """Initialize the cache with default data."""
        if not cls._cache_initialized:
            cls._cache['client'] = [
                {
                    "clientId": str(i),
                    "clientDesc": f"this is testing client {i}",
                    "clientName": f"Robinshood client {i if i <= 5 else 5}",
                    "clientSecret": "123456secret",
                    "scopeNameList": "fdx:read fdx:write",
                    "tppId": "TestAggregator",
                    "contacts": ["zanfu@bofa.com", "haha@bofa.com"],
                    "status": "active"
                }
                for i in range(1, 16)
            ]
            cls._cache_initialized = True

    @classmethod
    def add_to_cache(cls, item, cache_type):
        """Add a new item to the specified cache."""
        cls._cache[cache_type].append(item)

    @classmethod
    def update_cache(cls, item_id, updated_item, cache_type, id_field='clientId'):
        """Update an item in the specified cache."""
        for i, item in enumerate(cls._cache[cache_type]):
            if item[id_field] == item_id:
                cls._cache[cache_type][i] = updated_item
                return True
        return False

    @classmethod
    def delete_from_cache(cls, item_id, cache_type, id_field='clientId'):
        """Delete an item from the specified cache."""
        for i, item in enumerate(cls._cache[cache_type]):
            if item[id_field] == item_id:
                del cls._cache[cache_type][i]
                return True
        return False

    @classmethod
    def delete_client_batch(cls, client_ids: list) -> dict:
        """Delete multiple clients by their IDs."""
        success_ids = []
        failed_ids = []
        
        for client_id in client_ids:
            if cls.delete_from_cache(client_id, 'client'):
                success_ids.append(client_id)
            else:
                failed_ids.append(client_id)
        
        return {
            "status": "success" if not failed_ids else "partial",
            "deleted": success_ids,
            "failed": failed_ids,
            "message": f"Successfully deleted {len(success_ids)} clients, failed to delete {len(failed_ids)} clients"
        }

    @classmethod
    def get_client_data(cls):
        """Return client data from cache."""
        if not cls._cache_initialized:
            cls.initialize_cache()
        return cls._cache['client']

    @classmethod
    def get_client_by_id(cls, client_id):
        """Get a single client by ID."""
        clients = cls.get_client_data()
        return next((client for client in clients if client['clientId'] == client_id), None)

    @classmethod
    def get_env_data(cls):
        """Return environment data."""
        return [
            {"id": "1", "name": "dev 1"},
            {"id": "2", "name": "dev 2"},
            {"id": "3", "name": "sit 1"},
            {"id": "4", "name": "prod 1"}
        ]

    @classmethod
    def get_tpp_data(cls):
        """Return TPP data from cache."""
        if not cls._cache_initialized:
            cls.initialize_cache()
        if not cls._cache.get('tpp'):
            tpp_list = [
                Tpp(
                    tpp_id=f"TPP{i}",
                    tpp_name=f"Test TPP {i}",
                    tpp_type="Aggregator" if i % 2 == 0 else "Processor",
                    verified_client=f"client{i}",
                    scope_name_list="fdx:read fdx:write",
                    tpp_desc=f"This is test TPP number {i}"
                ) for i in range(1, 6)
            ]
            cls._cache['tpp'] = [tpp.to_dict() for tpp in tpp_list]
        return cls._cache['tpp']

    @classmethod
    def get_tpp_by_id(cls, tpp_id):
        """Get a single TPP by ID."""
        tpps = cls.get_tpp_data()
        return next((tpp for tpp in tpps if tpp['tppId'] == tpp_id), None)

    @classmethod
    def get_scope_data(cls):
        """Return scope data from cache."""
        if not cls._cache_initialized:
            cls.initialize_cache()
        if not cls._cache.get('scope'):
            scope_list = [
                Scope(
                    scope_name="fdx:read",
                    mapping_url="/api/fdx/read",
                    scope_desc="FDX Read Access Permission"
                ),
                Scope(
                    scope_name="fdx:write",
                    mapping_url="/api/fdx/write",
                    scope_desc="FDX Write Access Permission"
                ),
                Scope(
                    scope_name="fdx:admin",
                    mapping_url="/api/fdx/admin",
                    scope_desc="FDX Admin Access Permission"
                ),
                Scope(
                    scope_name="fdx:delete",
                    mapping_url="/api/fdx/delete",
                    scope_desc="FDX Delete Access Permission"
                )
            ]
            cls._cache['scope'] = [scope.to_dict() for scope in scope_list]
        return cls._cache['scope']
