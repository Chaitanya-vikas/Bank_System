from django.contrib import admin
from .models import Account, TransactionLog

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    # Change 'name' to 'user' because we are now using the User model
    list_display = ('id', 'user', 'balance') 
    search_fields = ('user__username',)  # Allow searching by username

@admin.register(TransactionLog)
class TransactionLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'sender', 'receiver', 'amount', 'status')
    list_filter = ('status',)
    ordering = ('-timestamp',)