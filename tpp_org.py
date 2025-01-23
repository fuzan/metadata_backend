from tpp import Tpp
from org import Org

class TppOrg:
    """Entity class representing a TPP-Organization relationship."""

    def __init__(self, org: Org, tpp: Tpp, tpp_org_id: str):
        """Initialize a new TPP-Organization relationship instance."""
        self.org = org
        self.tpp = tpp
        self.tpp_org_id = tpp_org_id

    def to_dict(self) -> dict:
        """Convert TppOrg instance to dictionary."""
        return {
            'org': self.org.to_dict(),
            'tpp': self.tpp.to_dict(),
            'tppOrgId': self.tpp_org_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TppOrg':
        """Create TppOrg instance from dictionary."""
        return cls(
            org=Org.from_dict(data.get('org', {})),
            tpp=Tpp.from_dict(data.get('tpp', {})),
            tpp_org_id=data.get('tppOrgId', '')
        )
