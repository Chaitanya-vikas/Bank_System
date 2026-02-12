import os
import django
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ibm_bank.settings")
django.setup()

User = get_user_model()
USERNAME = 'admin'
PASSWORD = 'admin123'  # Change this to a strong password!

if not User.objects.filter(username=USERNAME).exists():
    print(f"Creating new superuser: {USERNAME}")
    User.objects.create_superuser(USERNAME, 'admin@example.com', PASSWORD)
else:
    print("Superuser already exists. Skipping creation.")