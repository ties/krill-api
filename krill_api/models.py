import base64

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class KrillStatusInfo:
    version: str
    started: int

@dataclass
class CaHandle:
    handle: str

@dataclass
class KrillExchange:
    timestamp: int
    uri: str
    result: str
    
@dataclass
class KrillResources:
    asn: str
    ipv4: str
    ipv6: str

@dataclass(repr=False)
class KrillIssuedCert:
    uri: str
    req_limit: object
    cert: bytes
    
    @staticmethod
    def from_data(data: Dict[str, object]) -> 'KrillIssuedCert':
        cert = base64.b64decode(data['cert'])
        
        return KrillIssuedCert(uri=data.get('uri', data.get('url')), req_limit=data.get('req_limit', None), cert=cert)
    
    def __repr__(self) -> str:
        b64 = base64.b64encode(self.cert).decode('ascii')
        return f"KrillIssuedCert[uri={self.uri}, req_limit={self.req_limit}, cert='{b64[:8]}...{b64[-8:]}']"
    
@dataclass
class KrillResourceClass:
    class_name: str
    not_after: str
    issued_certs: List[KrillIssuedCert]
    signing_cert: KrillIssuedCert
    resource_set: KrillResources
    
    @staticmethod
    def from_data(data: Dict[str, object]) -> 'KrillResourceClass':
        return KrillResourceClass(
            class_name=data.get('class_name'),
            resource_set=KrillResources(**data.get('resource_set')),
            not_after=data.get('not_after'),
            issued_certs=[KrillIssuedCert.from_data(d) for d in data.get('issued_certs')],
            signing_cert=KrillIssuedCert.from_data(data.get('signing_cert'))
        )
    

    
@dataclass
class KrillParentHandle:
    handle: str
    parent_handle: str
    last_exchange: KrillExchange
    last_success: int
    all_resources: KrillResources
    classes: List[KrillResourceClass]

    
    @staticmethod
    def from_data(handle: str, parent_handle: str, body: Dict[str, object]) -> 'KrillParentHandle':
        return KrillParentHandle(
            handle=handle,
            parent_handle=parent_handle,
            last_exchange=KrillExchange(**body.get('last_exchange')),
            last_success=body.get('last_success'),
            all_resources=KrillResources(**body.get('all_resources')),
            classes=[KrillResourceClass.from_data(rc) for rc in body.get('classes')]
        )
    

@dataclass
class CaDeleteFailure:
    label: str
    msg: str
    args: Dict[str, object]