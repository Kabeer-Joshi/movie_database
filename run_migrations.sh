#!/bin/bash

# Activate the virtual environment if needed
# source /path/to/venv/bin/activate

# Create migrations
echo "Creating migrations..."
python3 manage.py makemigrations

# Apply migrations
echo "Applying migrations..."
python3 manage.py migrate

# Start the development server
echo "Starting the development server..."
python3 manage.py runserver