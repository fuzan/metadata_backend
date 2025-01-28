class BoaEnv:
    """Entity class representing an product and dev environment."""

    def __init__(self, id: str, name: str, site_id: str, is_still_using: bool):
        """Initialize a new env instance."""
        self.id = id
        self.name = name
        self.site_id = site_id
        self.is_still_using = is_still_using

    def to_dict(self) -> dict:
        """Convert environment instance to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'siteId': self.site_id,
            'stillUsing': self.is_still_using
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'BoaEnv':
        """Create environment instance from dictionary."""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            site_id=data.get('site_id', ''),
            is_still_using=data.get('isStillUsing', '')
        )
