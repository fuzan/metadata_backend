from entities.status import Status
from entities.tpp import Tpp
from entities.org import Org

class TppOrg:
    """Entity class representing a TPP-Organization relationship."""

    def __init__(self, org: Org, tpp: Tpp, tpp_org_id: str, status: Status = Status.ACTIVE):
        """Initialize a new TPP-Organization relationship instance."""
        self.org = org
        self.tpp = tpp
        self.tpp_org_id = tpp_org_id
        self.status = status

    def to_dict(self) -> dict:
        """Convert TppOrg instance to dictionary."""
        return {
            'org': self.org.to_dict(),
            'tpp': self.tpp.to_dict(),
            'tppOrgId': self.tpp_org_id,
            'status': self.status.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TppOrg':
        """Create TppOrg instance from dictionary."""
        return cls(
            org=Org.from_dict(data.get('org', {})),
            tpp=Tpp.from_dict(data.get('tpp', {})),
            tpp_org_id=data.get('tppOrgId', ''),
            status=Status(data.get('status', 'active'))
        )
