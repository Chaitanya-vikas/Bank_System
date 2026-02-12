from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from .models import Account, TransactionLog
from django.contrib.auth.models import User
import json
from decimal import Decimal

# --- AUTHENTICATION VIEWS ---
# In core/views.py

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # --- CHANGE THIS LINE ---
            # Old: Account.objects.create(user=user, balance=1000.00)
            # New: Start with Zero (Real World Logic)
            Account.objects.create(user=user, balance=0.00) 
            
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --- MAIN APP VIEWS ---

# In core/views.py

@login_required
def home(request):
    try:
        user_account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        user_account = Account.objects.create(user=request.user, balance=0)

    # --- OPTIMIZED QUERY ---
    # We use 'select_related' to fetch related Account and User data in ONE go.
    recent_transactions = TransactionLog.objects.select_related(
        'sender__user',   # Join Sender -> User table
        'receiver__user'  # Join Receiver -> User table
    ).filter(
        sender=user_account
    ).order_by('-timestamp')[:5]

    return render(request, 'index.html', {
        'account': user_account,
        'transactions': recent_transactions
    })

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            receiver_username = data.get('receiver_username') # User types NAME, not ID
            amount = Decimal(str(data.get('amount')))

            if amount <= 0: raise ValueError("Invalid amount.")
            
            with transaction.atomic():
                sender = Account.objects.select_for_update().get(user=request.user)
                
                # Find receiver by USERNAME (More realistic than ID)
                try:
                    receiver_user = User.objects.get(username=receiver_username)
                    receiver = Account.objects.select_for_update().get(user=receiver_user)
                except User.DoesNotExist:
                    raise ValueError("User not found.")

                if sender == receiver: raise ValueError("Cannot send to self.")
                if sender.balance < amount: raise ValueError("Insufficient funds.")

                # Execute Transfer
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()

                TransactionLog.objects.create(sender=sender, receiver=receiver, amount=amount, status="SUCCESS")

            return JsonResponse({'status': 'success', 'message': 'Transfer Complete!'})

        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)})

    return JsonResponse({'status': 'error'})