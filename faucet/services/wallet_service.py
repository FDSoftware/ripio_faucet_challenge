from faucet.models import Wallet


def get_airdrop_amount(wallet: Wallet):
    if wallet.faucet_reward_type == "AMOUNT":
        return wallet.faucet_reward_amount
    else:
        return wallet.last_balance * wallet.faucet_reward_percentage
