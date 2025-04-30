from entities.status import Status

class Client:
    """Entity class representing a Client."""
    
    # Create a single DAO instance for all client operations
    
    def __init__(self, client_id: str, client_name: str, client_desc: str,
                 tpp_id: str, client_secret: str, logo_uri: str, uri: str,
                 contacts: list, status: Status = Status.ACTIVE):
        """Initialize a new Client instance."""
        self.client_id = client_id
        self.client_name = client_name
        self.client_desc = client_desc
        self.tpp_id = tpp_id
        self.client_secret = client_secret
        self.logo_uri = logo_uri
        self.uri = uri
        self.contacts = contacts
        self.status = status

    def to_dict(self) -> dict:
        """Convert Client instance to dictionary."""
        return {
            'clientId': self.client_id,
            'clientName': self.client_name,
            'clientDesc': self.client_desc,
            'tppId': self.tpp_id,
            'clientSecret': self.client_secret,
            'logoUri': self.logo_uri,
            'uri': self.uri,
            'contacts': self.contacts,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Client':
        """Create Client instance from dictionary."""
        return cls(
            client_id=data.get('clientId', ''),
            client_name=data.get('clientName', ''),
            client_desc=data.get('clientDesc', ''),
            tpp_id=data.get('tppId', ''),
            client_secret=data.get('clientSecret', ''),
            logo_uri=data.get('logoUri', ''),
            uri=data.get('uri', ''),
            contacts=data.get('contacts', []),
            status=data.get('status', Status.ACTIVE)
        )

    @staticmethod
    def validate_fields(data: dict) -> None:
        """Validate client data fields."""
        required_fields = {
            'clientId': str,
            'clientName': str,
            'clientDesc': str,
            'tppId': str,
            'clientSecret': str,
            'logoUri': str,
            'uri': str,
            'contacts': list
        }

        for field, field_type in required_fields.items():
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(data[field], field_type):
                raise TypeError(f"Invalid type for {field}: expected {field_type.__name__}")
            if field == 'contacts' and not all(isinstance(x, str) for x in data[field]):
                raise TypeError("All contacts must be strings")
