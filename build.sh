#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files (CSS/Images) so the site looks good
python manage.py collectstatic --no-input

# Run database migrations (Create tables in your new Cloud MySQL)
python manage.py migrate