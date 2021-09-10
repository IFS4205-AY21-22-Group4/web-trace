# ifs4205-web-trace

Main web application for contact tracers, officials, token issuers, administrators.

## Usage

To test that the source code runs on a fresh Docker container, run:

```bash
docker-compose up --build -d
```

Apply migrations:

```bash
docker-compose run web python manage.py migrate # or run other commands as needed this way
docker-compose logs # Confirm that server runs without errors
```

When done:

```bash
docker-compose down
```

To delete database volume:

```bash
docker volume rm ifs4205-web-trace_mariadb_data
