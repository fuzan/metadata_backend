from client import Client
from tpp import Tpp, Status
from scope import Scope
from org import Org
from tpp_org import TppOrg
from boa_env import BoaEnv

class MockDataProducer:
    """Class to generate mock data for testing and development."""

    @staticmethod
    def generate_clients(count: int = 15) -> list:
        """Generate mock client data."""
        return [
            Client(
                client_id=str(i),
                client_name=f"Robinshood client {i if i <= 5 else 5}",
                client_desc=f"this is testing client {i}",
                tpp_id="TestAggregator",
                client_secret="123456secret",
                logo_uri="http://example.com/logo.png",
                uri="http://example.com",
                contacts=["zanfu@bofa.com", "haha@bofa.com"],
                status="active"
            ).to_dict()
            for i in range(1, count + 1)
        ]

    @staticmethod
    def generate_tpps(count: int = 5) -> list:
        """Generate mock TPP data."""
        return [
            Tpp(
                tpp_id=f"TPP{i}",
                tpp_name=f"Test TPP {i}",
                tpp_type="Aggregator" if i % 2 == 0 else "Processor",
                verified_client=f"client{i}",
                scope_name_list="fdx:read fdx:write",
                tpp_desc=f"This is test TPP number {i}",
                contact_name=f"Contact {i}",
                contact_email=f"contact{i}@example.com",
                status=Status.ACTIVE if i % 2 == 0 else Status.INACTIVE
            ).to_dict()
            for i in range(1, count + 1)
        ]

    @staticmethod
    def generate_scopes() -> list:
        """Generate mock scope data."""
        scope_configs = [
            ("fdx:read", "/api/fdx/read", "FDX Read Access Permission"),
            ("fdx:write", "/api/fdx/write", "FDX Write Access Permission"),
            ("fdx:admin", "/api/fdx/admin", "FDX Admin Access Permission"),
            ("fdx:delete", "/api/fdx/delete", "FDX Delete Access Permission")
        ]
        return [
            Scope(name, url, desc).to_dict()
            for name, url, desc in scope_configs
        ]

    @staticmethod
    def generate_orgs(count: int = 5) -> list:
        """Generate mock organization data."""
        return [
            Org(
                org_id=f"ORG{i}",
                customer_id_type_code="SSN" if i % 2 == 0 else "EIN",
                org_name=f"Organization {i}",
                org_desc=f"This is test organization number {i}",
                status="active" if i % 3 != 0 else "inactive"
            ).to_dict()
            for i in range(1, count + 1)
        ]

    @staticmethod
    def generate_tpp_org_relationships(tpps: list, orgs: list, count: int = 3) -> list:
        """Generate mock TPP-Org relationships."""
        relationships = []
        for i in range(min(count, len(tpps), len(orgs))):
            tpp = Tpp.from_dict(tpps[i])
            org = Org.from_dict(orgs[i])
            relationship = TppOrg(
                org=org,
                tpp=tpp,
                tpp_org_id=f"TPP_ORG_{i+1}"
            )
            relationships.append(relationship.to_dict())
        return relationships

    @staticmethod
    def generate_env_data() -> list:
        """Generate mock environment data."""
        env_configs = [
            ("1", "dev 1", "SITE001", True),
            ("2", "dev 2", "SITE002", True),
            ("3", "sit 1", "SITE003", False),
            ("4", "prod 1", "SITE004", True)
        ]
        return [
            BoaEnv(env_id, name, site_id, is_still_using).to_dict()
            for env_id, name, site_id, is_still_using in env_configs
        ]
