from django.db import models   # <--- THIS WAS MISSING
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} (${self.balance})"

class TransactionLog(models.Model):
    sender = models.ForeignKey(Account, related_name='sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, related_name='received', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="PENDING")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['sender', 'timestamp']),
        ]

    def __str__(self):
        return f"${self.amount} | {self.sender.user.username} -> {self.receiver.user.username}"