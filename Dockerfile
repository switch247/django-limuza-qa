# Use the specified Python version
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies for PostgreSQL and Node.js
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    git \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (use the LTS version or a specific version if needed)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

    RUN adduser --disabled-password --gecos '' django-user
# Set the working directory
WORKDIR /code

# Install Poetry and dependencies
RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction

# Copy the rest of the application code
COPY . /code

# Install JavaScript dependencies
COPY package.json package-lock.json /code/
RUN npm install

# Build Tailwind CSS (and other assets if needed)
# RUN npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify

# Collect static files for Django
RUN python manage.py collectstatic --noinput

# Expose the port for the application
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "limuza.wsgi"]