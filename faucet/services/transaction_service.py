from config.w3_init import async_w3


async def make_transaction(recipient, amount):
    return await async_w3.eth.send_transaction(
        {
            "to": recipient,
            "nonce": await get_nonce(),
            "value": async_w3.to_wei(amount, "ether"),
        }
    )


async def get_transaction(transaction_hash):
    return await async_w3.eth.get_transaction(transaction_hash)


async def get_nonce():
    return await async_w3.eth.get_transaction_count(async_w3.eth.default_account)
