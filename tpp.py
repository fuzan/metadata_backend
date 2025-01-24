from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Tpp:
    """Entity class representing a Third Party Provider (TPP)."""

    def __init__(self, tpp_id: str, tpp_name: str, tpp_type: str,
                 verified_client: str, scope_name_list: str, tpp_desc: str,
                 contact_name: str, contact_email: str, status: Status = Status.ACTIVE):
        """Initialize a new TPP instance."""
        self.tpp_id = tpp_id
        self.tpp_name = tpp_name
        self.tpp_type = tpp_type
        self.verified_client = verified_client
        self.scope_name_list = scope_name_list
        self.tpp_desc = tpp_desc
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.status = status

    def to_dict(self) -> dict:
        """Convert TPP instance to dictionary."""
        return {
            'tppId': self.tpp_id,
            'tppName': self.tpp_name,
            'tppType': self.tpp_type,
            'verifiedClient': self.verified_client,
            'scopeNameList': self.scope_name_list,
            'tppDesc': self.tpp_desc,
            'contactName': self.contact_name,
            'contactEmail': self.contact_email,
            'status': self.status.value
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Tpp':
        """Create TPP instance from dictionary."""
        return cls(
            tpp_id=data.get('tppId', ''),
            tpp_name=data.get('tppName', ''),
            tpp_type=data.get('tppType', ''),
            verified_client=data.get('verifiedClient', ''),
            scope_name_list=data.get('scopeNameList', ''),
            tpp_desc=data.get('tppDesc', ''),
            contact_name=data.get('contactName', ''),
            contact_email=data.get('contactEmail', ''),
            status=Status(data.get('status', 'active'))
        )
