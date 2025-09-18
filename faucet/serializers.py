from rest_framework import serializers
from web3 import Web3

from .models.transaction import Transaction


class TransactionCreateSerializer(serializers.ModelSerializer):
    def validate_recipient(self, value):
        if not Web3.is_address(value):
            raise serializers.ValidationError("Recipient address is invalid!")
        return value

    class Meta:
        model = Transaction
        fields = ["recipient"]


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "hash",
            "status",
            "recipient",
            "amount",
            "timestamp",
            "nonce",
            "gasPrice",
        ]


def get_serialized_transactions(db_results):
    serializer = TransactionRetrieveSerializer(db_results, many=True)
    return serializer.data
