from django.test import TestCase
from rest_framework.exceptions import ValidationError

from faucet.serializers import (
    TransactionCreateSerializer,
    TransactionRetrieveSerializer,
    get_serialized_transactions,
)
from faucet.models.transaction import Transaction


class TransactionCreateSerializerTest(TestCase):
    def test_valid_recipient_address(self):
        """Test that a valid Ethereum address is accepted."""
        valid_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        serializer = TransactionCreateSerializer(data={"recipient": valid_address})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["recipient"], valid_address)

    def test_invalid_recipient_address(self):
        """Test that an invalid Ethereum address raises a validation error."""
        invalid_addresses = [
            "0x742d35Cc6634C0532925a3b844Bc454e4438f44",  # Too short
            "0xZZZd35Cc6634C0532925a3b844Bc454e4438f44e",  # Invalid characters
            "invalid_address",  # Completely invalid
        ]

        for address in invalid_addresses:
            serializer = TransactionCreateSerializer(data={"recipient": address})
            with self.assertRaises(ValidationError):
                serializer.is_valid(raise_exception=True)


class TransactionRetrieveSerializerTest(TestCase):
    def setUp(self):
        """Create a sample transaction for testing."""
        self.transaction = Transaction.objects.create(
            hash="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            recipient="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            amount=1.5,
            nonce=1,
            status="PENDING",
            gasPrice=20000000000,
            gasUsed=21000,
        )

    def test_serializer_contains_expected_fields(self):
        """Test that the serializer includes all expected fields."""
        serializer = TransactionRetrieveSerializer(instance=self.transaction)
        expected_fields = [
            "hash",
            "status",
            "recipient",
            "amount",
            "timestamp",
            "nonce",
            "gasPrice",
            "gasUsed",
        ]
        self.assertEqual(set(serializer.data.keys()), set(expected_fields))


class GetSerializedTransactionsTest(TestCase):
    def setUp(self):
        self.transaction1 = Transaction.objects.create(
            hash="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            recipient="0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            amount=1.5,
            nonce=1,
            status="PENDING",
            gasPrice=20000000000,
            gasUsed=21000,
        )

        self.transaction2 = Transaction.objects.create(
            hash="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            recipient="0x942d35Cc6634C0532925a3b844Bc454e4438f44f",
            amount=2.0,
            nonce=2,
            status="MINED",
            gasPrice=25000000000,
            gasUsed=25000,
        )

    def test_get_serialized_transactions(self):
        transactions = Transaction.objects.all()
        serialized_data = get_serialized_transactions(transactions)

        # fields of the serializer are tested in TransactionRetrieveSerializerTest, so only check length here.
        self.assertEqual(len(serialized_data), 2)
