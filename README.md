# Fygo Demo

## Setup instructions

### Pyenv

Ensure you have Pyenv installed.

```
pyenv install 3.9.5
pyenv global 3.9.5
pyenv virtualenv fygo-demo
```

When you `cd` into the project directory Pyenv will switch to the `fygo-demo` virtualenv for you.

### Python dependencies for IDE/editor development

```
pip install -r demo/requirements.txt
pip install -r demo/requirements-dev.txt
```

This will resolve dependencies locally for code analysis in your IDE/editor.

### Local development setup via Docker

Run local development server in Docker for a consistent development experience with a Postgres database setup.

First ensure you have Docker desktop installed.

From the project root, run the following to create the database on the running Postgres container:

```
docker-compose up
docker-compose exec db sh
su - postgres -c psql
CREATE DATABASE demodb OWNER postgres;
exit
exit
```

And run the following to initialise and migrate database tables and create a root admin user:

```
docker-compose exec web sh -c './manage.py migrate'
docker-compose exec web sh -c './manage.py createsuperuser'
```

## Local development

Just run the following to start a hot-reloading development server accessible on http://localhost:8000.

```
docker-compose up
```

Django server errors will be shown in the output.

When you're finished, just Ctrl-C that process.