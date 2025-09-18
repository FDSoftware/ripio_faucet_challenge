from celery import shared_task
from web3.exceptions import TransactionNotFound

from config.w3_init import sync_w3, async_w3
from faucet.models import Transaction, Wallet


@shared_task
def update_transaction_result(transaction_hash):
    try:
        transaction_data = sync_w3.eth.wait_for_transaction_receipt(transaction_hash)
        transaction_model = Transaction.objects.get(hash=transaction_hash)

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
def track_wallet_balance():
    wallet_address = async_w3.eth.default_account

    wallet_balance = sync_w3.eth.get_balance(wallet_address)
    wallet_nonce = sync_w3.eth.get_transaction_count(wallet_address)

    wallet_model = Wallet.objects.get(pk=1)
    wallet_model.last_balance = sync_w3.from_wei(wallet_balance, "ether")
    wallet_model.nonce = wallet_nonce

    wallet_model.save()
