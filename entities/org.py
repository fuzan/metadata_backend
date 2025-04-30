from entities.status import Status

class Org:
    """Entity class representing an Organization."""

    def __init__(self, org_id: str, customer_id_type_code: str,
                 org_name: str, org_desc: str, status: Status = Status.ACTIVE):
        """Initialize a new Organization instance."""
        self.org_id = org_id
        self.customer_id_type_code = customer_id_type_code
        self.org_name = org_name
        self.org_desc = org_desc
        self.status = status

    def to_dict(self) -> dict:
        """Convert Organization instance to dictionary."""
        return {
            'orgId': self.org_id,
            'customerIdTypeCode': self.customer_id_type_code,
            'orgName': self.org_name,
            'orgDesc': self.org_desc,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Org':
        """Create Organization instance from dictionary."""
        return cls(
            org_id=data.get('orgId', ''),
            customer_id_type_code=data.get('customerIdTypeCode', ''),
            org_name=data.get('orgName', ''),
            org_desc=data.get('orgDesc', ''),
            status=data.get('status', Status.ACTIVE)
        )
