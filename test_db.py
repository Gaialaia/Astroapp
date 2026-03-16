import os
import django
import subprocess

# 1. Get a fresh token from 'yc'
try:
    token = subprocess.check_output(['yc', 'iam', 'create-token']).decode('utf-8').strip()
except:
    token = "PASTE_YOUR_TOKEN_HERE" # Backup if yc command fails

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astroknow.settings')
django.setup()

from django.conf import settings
from django.db import connection

# 2. Force the token into the database options for this test
settings.DATABASES['default']['OPTIONS']['iam_token'] = token

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("Connection Successful! Result:", cursor.fetchone())
except Exception as e:
    print(f"Connection Failed: {e}")
