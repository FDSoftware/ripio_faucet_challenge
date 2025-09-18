from web3 import AsyncWeb3, AsyncHTTPProvider, Web3, HTTPProvider
from web3.middleware import SignAndSendRawMiddlewareBuilder

from config.settings import env

async_w3 = AsyncWeb3(AsyncHTTPProvider(env("ETH_RPC_URL")))
sync_w3 = Web3(HTTPProvider(env("ETH_RPC_URL")))


def init_web3():
    acct = async_w3.eth.account.from_key(env("ETH_SECRET_KEY"))
    async_w3.middleware_onion.inject(
        SignAndSendRawMiddlewareBuilder.build(acct), layer=0
    )
    async_w3.eth.default_account = acct.address
