from django.db import models

faucet_reward_type = {"PERCENTAGE": "percentage", "AMOUNT": "fixed amount"}


class Wallet(models.Model):
    faucet_reward_type = models.CharField(choices=faucet_reward_type, default="AMOUNT")
    faucet_reward_amount = models.DecimalField(
        max_digits=36, decimal_places=18, default=0.000005
    )
    faucet_reward_percentage = models.DecimalField(
        max_digits=7, decimal_places=4, default=0
    )
    last_balance = models.DecimalField(max_digits=36, decimal_places=18, default=0)

    nonce = models.IntegerField(default=0)

    maxFeePerGas = models.IntegerField(
        help_text="Maximum allowed gas price in wei", default=1100000
    )

    def save(self, *args, **kwargs):
        if self.pk is not None:
            super().save(*args, **kwargs)
        else:
            self.pk = 1
            self.save()

    def __str__(self):
        return "Wallet ETH"
