import aiohttp
import itertools
import logging
import ssl
import urllib


from contextlib import asynccontextmanager
from typing import Dict, Optional, List

from .models import KrillApiError, KrillParentHandle, KrillCaStatus, CaHandle, KrillStatusInfo

LOG = logging.getLogger(__name__)


class KrillApiSessionClient:
    session: aiohttp.ClientSession
    base_url: str
    ssl: Optional[aiohttp.Fingerprint] = None
    
    def __init__(self, session: aiohttp.ClientSession, base_url: str, ssl: Optional[aiohttp.Fingerprint] = None) -> None:
        self.session = session
        self.base_url = base_url
        self.ssl = ssl
        
    @asynccontextmanager
    async def __request(self, method: str, relative_path: str) -> aiohttp.ClientResponse:
        async with self.session.request(method, urllib.parse.urljoin(self.base_url, relative_path), ssl=self.ssl) as res:
            yield res       

    async def info(self) -> object:
        async with self.__request('GET', '/stats/info') as res:
            return await res.json()
        
    async def list(self) -> object:
        async with self.__request('GET', '/api/v1/cas') as res:
            return [
                CaHandle(**handle)
                for handle in (await res.json())['cas']
            ]
    
    async def ca_status(self, handle: str) -> KrillCaStatus:
        async with self.__request('GET', f"/api/v1/cas/{handle}") as res:
            body = await res.json()
            if res.status != 200:
                raise KrillApiError(**body)
            return KrillCaStatus.from_data(body)
        
    async def ca_parent_status(self, handle: str) -> List[KrillParentHandle]:
        async with self.__request('GET', f"/api/v1/cas/{handle}/parents") as res:
            res = await res.json()
            return [
                KrillParentHandle.from_data(handle, k, v) for k, v in res.items()
            ]

    async def ca_delete(self, handle: str) -> bool:
        async with self.__request('DELETE', f"/api/v1/cas/{handle}") as res:
            if res.status == 200:
                return True
            else:
                LOG.debug("HTTP %s on DELETE for %s", res.status, handle)
                body = await res.json()
                
                raise KrillApiError(**body)
            
    async def info(self) -> KrillStatusInfo:
        async with self.__request('GET', '/stats/info') as res:
            res = await res.json()
            return KrillStatusInfo(**res)


@asynccontextmanager
async def KrillApiClient(base_url: str, token: str, ssl: Optional[aiohttp.Fingerprint]=None):
    async with aiohttp.ClientSession(headers={'Authorization': f"Bearer {token}", "Accept": "application/json"}) as session:
        yield KrillApiSessionClient(session, base_url, ssl)
    