#!/bin/bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create mediafiles directory if it doesn't exist
mkdir -p mediafiles/products

# Copy media files
cp -r media/products/* mediafiles/products/

# Convert static asset files
python manage.py collectstatic --noinput

# Apply any outstanding database migrations
python manage.py migrate
