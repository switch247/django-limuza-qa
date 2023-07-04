#!/bin/bash

# Step 1: Delete migration files
echo "Deleting migration files..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -exec rm -f {} +
find . -path "*/migrations/*.pyc" -exec rm -f {} +

# Step 2: Drop the database
echo "Dropping the database..."
psql -U postgres -c "DROP DATABASE IF EXISTS limuza;"

# Step 3: Create the database
echo "Creating the database..."
psql -U postgres -c "CREATE DATABASE limuza OWNER tauhir;"

# Step 4: Run initial migrations
echo "Running initial migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Done!"