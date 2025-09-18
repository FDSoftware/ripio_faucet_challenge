import unittest
from decimal import Decimal
from unittest.mock import Mock

from django.test import TestCase

from faucet.models import Wallet
from faucet.services.wallet_service import get_airdrop_amount


class TestWalletService(TestCase):
    def test_get_airdrop_amount_with_amount_type(self):
        mock_wallet = Mock(spec=Wallet)
        mock_wallet.faucet_reward_type = "AMOUNT"
        mock_wallet.faucet_reward_amount = Decimal("0.000005")

        result = get_airdrop_amount(mock_wallet)

        self.assertEqual(result, Decimal("0.000005"))

    def test_get_airdrop_amount_with_percentage_type(self):
        mock_wallet = Mock(spec=Wallet)
        mock_wallet.faucet_reward_type = "PERCENTAGE"
        mock_wallet.last_balance = Decimal("1.0")
        mock_wallet.faucet_reward_percentage = Decimal("0.05")  # 5%

        result = get_airdrop_amount(mock_wallet)

        expected = Decimal("1.0") * Decimal("0.05")
        self.assertEqual(result, expected)

    def test_get_airdrop_amount_with_zero_balance(self):
        # Test with zero balance
        mock_wallet = Mock(spec=Wallet)
        mock_wallet.faucet_reward_type = "PERCENTAGE"
        mock_wallet.last_balance = Decimal("0")
        mock_wallet.faucet_reward_percentage = Decimal("0.05")

        result = get_airdrop_amount(mock_wallet)

        # Result should be zero
        self.assertEqual(result, Decimal("0"))


if __name__ == "__main__":
    unittest.main()
