from django.contrib import admin
from django.shortcuts import redirect

from faucet.models import Wallet, Transaction
# Register your models here.


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    readonly_fields = ["last_balance", "nonce"]

    def changelist_view(self, request, extra_context=None):
        first_object = Wallet.objects.get_or_create()
        return redirect("admin:faucet_wallet_change", object_id=first_object[0].pk)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
