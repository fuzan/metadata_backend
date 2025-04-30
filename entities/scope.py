class Scope:
    """Entity class representing a Scope."""

    def __init__(self, scope_name: str, mapping_url: str, scope_desc: str):
        """Initialize a new Scope instance."""
        self.scope_name = scope_name
        self.mapping_url = mapping_url
        self.scope_desc = scope_desc

    def to_dict(self) -> dict:
        """Convert Scope instance to dictionary."""
        return {
            'scopeName': self.scope_name,
            'mappingUrl': self.mapping_url,
            'scopeDesc': self.scope_desc
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Scope':
        """Create Scope instance from dictionary."""
        return cls(
            scope_name=data.get('scopeName', ''),
            mapping_url=data.get('mappingUrl', ''),
            scope_desc=data.get('scopeDesc', '')
        )
