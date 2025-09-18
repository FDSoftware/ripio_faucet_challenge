from unittest.mock import patch, MagicMock

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from faucet.models import Wallet, Transaction


class TestTransactionApi(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.transaction_list_url = "/api/airdrops/"

    def test_get_airdrops(self):
        Transaction.objects.create(hash="abc", amount=100, nonce=1)
        Transaction.objects.create(hash="def", amount=50, nonce=2)

        response = self.client.get(self.transaction_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch("faucet.views.make_transaction")
    @patch("faucet.views.get_transaction")
    @patch("faucet.views.update_transaction_result.delay_on_commit")
    def test_post_airdrop_success(
        self, mock_delay_on_commit, mock_get_transaction, mock_make_transaction
    ):
        Wallet.objects.create(pk=1)  # faucet configuration
        mock_make_transaction.return_value = MagicMock(hex=lambda: "0x123")
        mock_get_transaction.return_value = MagicMock(gasPrice=5000000)

        response = self.client.post(
            self.transaction_list_url,
            {"recipient": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"},
            format="json",
        )

        # check api response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("hash", response.data)

        # check database
        transaction = Transaction.objects.first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.hash, "0x123")

    @patch("faucet.views.make_transaction")
    @patch("faucet.views.get_transaction")
    @patch("faucet.views.update_transaction_result.delay_on_commit")
    def test_post_airdrop_invalid_address(
        self, mock_delay_on_commit, mock_get_transaction, mock_make_transaction
    ):
        Wallet.objects.create(pk=1)  # faucet configuration
        mock_make_transaction.return_value = MagicMock(hex=lambda: "0x123")
        mock_get_transaction.return_value = MagicMock(gasPrice=5000000)

        response = self.client.post(
            self.transaction_list_url,
            {"recipient": "0xRecipientAddress"},
            format="json",
        )

        # invalid address should return 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_airdrop_no_configuration(self):
        response = self.client.post(
            self.transaction_list_url,
            {"recipient": "0xRecipientAddress"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # test error message:
        self.assertIn("Faucet configuration not found!", str(response.data))
