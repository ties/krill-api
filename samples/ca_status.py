import logging
import os
import sys

from pathlib import Path

# Add working dir to path
sys.path.insert(0,os.environ['PWD'])

logging.basicConfig()
logging.getLogger('matplotlib').setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.DEBUG)

LOG = logging.getLogger(__name__)

import itertools
import hashlib
import logging
import os
import ssl
import time


import aiohttp
import asyncio

from contextlib import asynccontextmanager

from krill_api import KrillApiClient

TOKEN = os.environ['KRILL_TOKEN']
KRILL_URL = os.environ['KRILL_URL']
KRILL_CERT_PATH = os.environ['KRILL_CERT_PATH']

# Dump the certificate in DER format like
# > openssl s_client -showcerts \
#     -servername krill.host \
#     -connect krill.host:3000 2>/dev/null | openssl x509 -inform pem -outform DER -out {KRILL_CERT_PATH}.der
#


with (Path(__file__).parent / KRILL_CERT_PATH).open('rb') as f:
    digest = hashlib.sha256(f.read()).digest()


async def run():
    async with KrillApiClient(KRILL_URL, TOKEN, aiohttp.Fingerprint(digest)) as client:
        res = await client.ca_status("krill_publisher_681597296374")
        print(res)

asyncio.run(run())