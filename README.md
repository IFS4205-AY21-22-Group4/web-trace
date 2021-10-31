# ifs4205-web-trace

Main web application for contact tracers, officials, token issuers, administrators.

## Usage

Ensure that ifs4205-database container is up and running first.

Start the container using `docker-compose`:

```bash
docker-compose up --build -d
```

To interact directly with the container using a terminal:

```bash
docker-compose exec web /bin/bash
```

To stop the container:

```bash
docker-compose stop
```

To tear down the container:

```bash
docker-compose down
```
