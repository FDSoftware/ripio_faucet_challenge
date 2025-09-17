from django.db import models

transaction_status = {
    "PENDING": "pending",
    "MINED": "mined",
    "CONFIRMED": "confirmed",
    "FAILED": "failed",
}


class Transaction(models.Model):
    hash = models.CharField(max_length=255, unique=True)
    recipient = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=36, decimal_places=18)
    timestamp = models.DateTimeField(auto_now_add=True)
    nonce = models.IntegerField()
    status = models.CharField(choices=transaction_status, default="PENDING")
    gasPrice = models.IntegerField(help_text="Gas price in wei", default=0)
