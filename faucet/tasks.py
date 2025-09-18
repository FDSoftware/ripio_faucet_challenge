from celery import shared_task
from web3.exceptions import TransactionNotFound

from config.w3_init import async_w3
from faucet.models import Transaction, Wallet


@shared_task
async def update_transaction_result(transaction_hash):
    try:
        transaction_data = await async_w3.eth.get_transaction_receipt(transaction_hash)
        transaction_model = Transaction.objects.get(transaction_hash=transaction_hash)

        transaction_model.gasUsed = transaction_data["gasUsed"]

        if transaction_data["status"] == 0:
            transaction_model.status = "FAILED"
        else:
            # todo: also check the first block mined and use "MINED" status?
            transaction_model.status = "CONFIRMED"

        transaction_model.save()
        # trigger celery task for updating wallet balance:
        track_wallet_balance.delay()

    except TransactionNotFound:
        # just re-throw the exception:
        raise TransactionNotFound(f"Transaction not found: {transaction_hash}")


@shared_task
async def track_wallet_balance():
    wallet_address = async_w3.eth.default_account
    wallet_balance = await async_w3.eth.get_balance(wallet_address)
    wallet_nonce = await async_w3.eth.get_transaction_count(wallet_address)

    wallet_model = Wallet.objects.get(address=wallet_address)
    wallet_model.last_balance = wallet_balance
    wallet_model.nonce = wallet_nonce

    wallet_model.save()
