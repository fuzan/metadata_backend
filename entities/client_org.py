from entities.status import Status
from entities.client import Client
from entities.org import Org

class ClientOrg:
    """Entity class representing a Client-Organization relationship."""

    def __init__(self, org: Org, client: Client, client_org_id: str, status: Status = Status.ACTIVE):
        """Initialize a new Client-Organization relationship instance."""
        self.org = org
        self.client = client
        self.client_org_id = client_org_id
        self.status = status

    def to_dict(self) -> dict:
        """Convert ClientOrg instance to dictionary."""
        return {
            'org': self.org.to_dict(),
            'client': self.client.to_dict(),
            'clientOrgId': self.client_org_id,
            'status': self.status.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ClientOrg':
        """Create ClientOrg instance from dictionary."""
        return cls(
            org=Org.from_dict(data.get('org', {})),
            client=Client.from_dict(data.get('client', {})),
            client_org_id=data.get('clientOrgId', ''),
            status=Status(data.get('status', 'active'))
        )
