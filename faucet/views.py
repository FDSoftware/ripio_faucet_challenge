from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from eth.exceptions import TransactionNotFound

from rest_framework import status
from rest_framework.response import Response
from adrf.views import APIView

from faucet.models import Transaction, Wallet
from faucet.serializers import TransactionCreateSerializer, get_serialized_transactions
from faucet.services.transaction_service import (
    make_transaction,
    get_nonce,
    get_transaction,
)
from faucet.services.wallet_service import get_airdrop_amount
from faucet.tasks import update_transaction_result


class TransactionApi(APIView):
    async def get(self, request):
        transactions = Transaction.objects.all()
        serializer = await sync_to_async(get_serialized_transactions)(transactions)

        return Response(serializer, status=status.HTTP_200_OK)

    async def post(self, request):
        serializer = await sync_to_async(TransactionCreateSerializer)(data=request.data)

        try:
            faucet_configuration = await sync_to_async(Wallet.objects.get)(pk=1)
        except ObjectDoesNotExist:
            # fail fast in case of non-configured faucet:
            return Response(
                {"error": "Faucet configuration not found!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            # get airdrop amount from configuration:
            airdrop_amount = get_airdrop_amount(faucet_configuration)

            # make transaction:
            try:
                transaction_hash = await make_transaction(
                    serializer.validated_data["recipient"], airdrop_amount
                )
                transaction_hex = transaction_hash.hex()
                transaction_data = await get_transaction(transaction_hex)
            except TransactionNotFound:
                return Response(
                    {"error": "Transaction failed!"}, status=status.HTTP_400_BAD_REQUEST
                )

            # complete the model data:
            serializer.validated_data["hash"] = transaction_hex
            serializer.validated_data["amount"] = airdrop_amount
            serializer.validated_data["nonce"] = await get_nonce()
            serializer.validated_data["gasPrice"] = transaction_data.gasPrice
            serializer.validated_data["gasUsed"] = (
                0  # 0 as the transaction is not yet confirmed.
            )

            await sync_to_async(serializer.save)()

            # trigger celery task to await transaction confirmation:
            await sync_to_async(update_transaction_result.delay_on_commit)(
                transaction_hex
            )

            return Response({"hash": transaction_hex}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
