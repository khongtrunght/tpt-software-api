# TPT Payroll API

## Backend local development, additional details

### General workflow

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

You can install all the dependencies with:

```
pip install poetry
```

```console
poetry install
```

- To run, first create a `.env` file with the following content:

```env
SECRET_KEY=8e29206652ffd60c99f34b1aa85e15cb1d92cf2ef95306c82728882f7ad7647b
# Postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=payroll
POSTGRES_USER=root
POSTGRES_PASSWORD=secret
SUPERUSER=admin@admin.com
SUPERUSER_PASSWORD=tpt@123
```

- Then, run the following command to create the database:

```console
python -m payroll.cli database init
```

- Finally, run the following command to start the server:

```console
python -m bin.run
```

or develop with the following command:

```console
uvicorn payroll.main:app --reload
```
