from mock_data import MockDataProducer

class CacheStorage:
    """Class to manage all data operations through cache."""
    
    _cache = {
        'client': [],
        'tpp': [],
        'scope': [],
        'org': [],
        'tppOrg': [],
        'env': []  # Add env to cache
    }
    _cache_initialized = False

    @classmethod
    def initialize_cache(cls):
        """Initialize the cache with default data."""
        if not cls._cache_initialized:
            # Load all mock data at startup
            cls._cache['client'] = MockDataProducer.generate_clients()
            cls._cache['tpp'] = MockDataProducer.generate_tpps()
            cls._cache['scope'] = MockDataProducer.generate_scopes()
            cls._cache['org'] = MockDataProducer.generate_orgs()
            cls._cache['env'] = MockDataProducer.generate_env_data()
            # TPP-Org relationships need TPP and Org data
            cls._cache['tppOrg'] = MockDataProducer.generate_tpp_org_relationships(
                cls._cache['tpp'],
                cls._cache['org']
            )
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

    # Remove delete_client_batch method as it's now in Client class

    @classmethod
    def get_env_data(cls):
        """Return environment data from cache."""
        if not cls._cache_initialized:
            cls.initialize_cache()
        return cls._cache['env']

    @classmethod
    def get_tpp_data(cls):
        """Return TPP data from cache."""
        if not cls._cache_initialized:
            cls.initialize_cache()
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
        return cls._cache['scope']

    @classmethod
    def get_org_data(cls):
        """Return organization data from cache."""
        if not cls._cache_initialized:
            cls.initialize_cache()
        return cls._cache['org']

    @classmethod
    def get_tpp_org_data(cls):
        """Return TPP-Organization relationship data from cache."""
        if not cls._cache_initialized:
            cls.initialize_cache()
        return cls._cache['tppOrg']
