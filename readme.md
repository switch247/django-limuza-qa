# MartialQA

## Overview

Customer Service Team analytics and quality assurance software

Here’s how you can update your README to include the instructions you provided:

---

## Installation Guide

### 1. Docker Setup
#### Docker installation (for Ubuntu)

Install Docker first [docker](https://linuxconfig.org/how-to-install-docker-on-ubuntu-22-04)

To install docker-compose:
```sudo apt-get install docker-compose-v2```

Alternative instructions for [docker compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04) here.



If you are getting error about curl command, install [curl](https://www.tecmint.com/bash-curl-command-not-found-error/). Please pay attention if you are using different shell than bash, for example zsh.


To build and run the application using Docker, follow these steps:

1. **Build the Docker Containers:**
Docker version 2 does not use dash anymore, some systems have migrated to command `docker compose build` or `docker compose up`

   ```bash
   docker-compose build
   ```

2. **Run the Docker Containers:**

   ```bash
   docker-compose up
   ```
   alternative command for some os versions:
   ```
   docker compose up
   ```

3. **Load initial data (needed to create any users):**

   Go inside web container
   ```
   docker exec -it limuza-web-1 bash
   ```

   Run management commands:

   ```
   python3 manage.py initial_setup
   python3 manage.py runscript -v2 initialise_data
   ```

4. **Access the Application:**
   The application will be accessible at `http://localhost:8000`. or `http://127.0.0.1:8000/`
   to run management commands you need to go inside web container:
   `docker exec -it limuza-web-1 bash`


4. Possible problems with docker:
   Docker version 2 does not use dash anymore, some systems have migrated to command `docker compose build` or `docker compose up`

   If running `docker compose build` returns error "compose is not a docker command", while `docker compose version` gives you compose version, see various possible fixes [here](https://github.com/docker/compose/issues/8630).


3. **Access the Application:**
   The application will be accessible at `http://127.0.0.1:8000`.

4. **Login with Test Credentials:**
   - **Username:** `james.bond@example.com`
   - **Password:** `topsecret`

   After logging in, you will be prompted to verify your email. The verification code will be displayed in your terminal. Copy the code from the logs and paste it into the email verification field in the application.

   Example log entry:

   ```
   To confirm this is correct, go to http://127.0.0.1:8000/accounts/confirm-email/MQ:1sg85m:KueBp1-vy51D12E0K4ABpeAqGv8N-F0pSUrXLe-Uu0E/
   ```



#### Resetting Migrations

If you need to wipe and reset migrations:

```bash
find ./your_project_directory -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./path_to_exclude/*" -delete
find ./your_project_directory -path "*/migrations/*.pyc" -not -path "./path_to_exclude/*" -delete
python manage.py reset_db
python manage.py makemigrations
```
### 2.Local Setup Without Docker
<details>

<summary>Click here for guide</summary>


#### Step 1: System Requirements

Ensure your system is up to date:

```bash
sudo apt-get update
sudo apt-get -y upgrade
```

Install the required system packages:

```bash
sudo apt-get install build-essential checkinstall libffi-dev python2-dev python2 python-dev-is-python3 -y
sudo apt-get install libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev python3-openssl -y
```

#### Step 2: Python Setup

1. **Install pyenv:**

   ```bash
   git clone https://github.com/pyenv/pyenv.git ~/.pyenv
   ```

2. **Configure pyenv:**

   For Bash:

   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
   echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
   echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bash_profile
   ```

   For Zsh:

   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
   echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   echo 'eval "$(pyenv init -)"' >> ~/.zshrc
   ```

   Reload the shell:

   ```bash
   exec "$SHELL"
   ```

3. **Install and Set Python Version:**

   ```bash
   pyenv install 3.12.3
   pyenv global 3.12.3
   ```

4. **Create a Virtual Environment:**

   ```bash
   pyenv exec python -m venv venv
   source venv/bin/activate
   ```

#### Step 3: Install Dependencies

1. **Install pipx:**

   ```bash
   sudo apt update
   sudo apt install pipx
   pipx ensurepath
   ```

2. **Install Poetry:**

   ```bash
   pipx install poetry
   poetry install
   ```

3. **Install PostgreSQL:**

   ```bash
   sudo apt install postgresql
   ```

   Refer to the [PostgreSQL setup guide](https://betterstack.com/community/guides/scaling-python/django-postgresql/#step-3-setting-up-a-postgresql-database) for detailed instructions.

4. **Install npm and Node.js:**

   Install npm:

   ```bash
   sudo apt install npm
   ```

   Install Node Version Manager (NVM):

   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
   ```

   Install Node.js:

   ```bash
   nvm install 20
   ```

   Verify Node.js and npm versions:

   ```bash
   node -v # should print `v20.14.0`
   npm -v # should print `10.7.0`
   ```

#### Step 4: Install Tailwind CSS and JS Libraries

1. **Install Tailwind CSS and Other Dependencies:**

   Ensure your `package.json` is configured with the necessary dependencies:

   ```json
   {
     "devDependencies": {
       "daisyui": "^4.12.10",
       "tailwindcss": "^3.4.4"
     },
     "dependencies": {
       "@alpinejs/persist": "^3.14.0",
       "@fortawesome/fontawesome-svg-core": "^6.5.2",
       "@fortawesome/free-brands-svg-icons": "^6.5.2",
       "@fortawesome/free-regular-svg-icons": "^6.5.2",
       "@fortawesome/free-solid-svg-icons": "^6.5.2",
       "alpinejs": "^3.14.0",
       "apexcharts": "^3.49.1",
       "flowbite": "^2.3.0"
     }
   }
   ```

   Install the dependencies:

   ```bash
   npm install
   ```

2. **Run Tailwind in Watch Mode (for Development):**

   ```bash
   npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch
   ```

### 3. Running the Application

#### First-Time Setup:

1. **Collect Static Files:**

   ```bash
   python manage.py collectstatic
   ```

2. **Update Dependencies:**

   ```bash
   poetry update
   ```

3. **Install and Migrate:**

   ```bash
   poetry install --no-root
   python manage.py migrate
   ```

4. **Run the Servers:**

   In separate terminal tabs:

   Tab 1: Run Django development server

   ```bash
   python manage.py runserver
   ```

   Tab 2: Run Tailwind in watch mode

   ```bash
   npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch
   ```

#### Regular Run:

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch
python manage.py runserver
```
</details>

### 4. Deployment

Deploy the application with:

```bash
fly deploy
```

### 5. Email Setup

In the deployed environment, set the following environment variables in `.env`:

```bash
EMAIL_HOST_USER=<your-email@example.com>
EMAIL_HOST_PASS=<your-app-password>
EMAIL_HOST=<smtp.example.com>
```

Refer to [this guide](#sending-emails) for instructions on setting up email credentials with Gmail or another provider.

### 6. Wiping Migrations

To wipe all migrations:

```bash
find ./apps -path "*/migrations/*.py" -not -name "__init__.py" -delete
find ./apps -path "*/migrations/*.pyc" -delete
```

### 7. Adding New Packages

Add new packages with Poetry:

```bash
poetry add <package>
poetry install --no-root
```

### Library Documentation

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [ApexCharts Documentation](https://apexcharts.com/docs)
- [DaisyUI Documentation](https://daisyui.com/components)
- [Flowbite Documentation](https://flowbite.com/docs/getting-started/introduction/)
