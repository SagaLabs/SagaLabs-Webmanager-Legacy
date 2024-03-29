# SagaLabs Web Manager Legacy
This is the old and open-source version of SagaLabs webmanager. 


Written in Flask

## Usage

On both linux and windows login using the az-cli command

```bash
az login
```

**Linux**

```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
flask run
```

**Windows (PowerShell)**

```ps1
virtualenv venv
./venv/Scripts/activate
pip install -r requirements.txt
flask run
```

## Docker

Make a file called .env with the variables for a service-principal in the root directory.
The file should set the following variables:

```bash
AZURE_CLIENT_ID=<your-service-principal-client-id>
AZURE_CLIENT_SECRET=<your-service-principal-client-secret>
AZURE_TENANT_ID=<your-azure-tenant-id>
```

```bash
docker-compose up --build
```

The `-it` makes the instance interactive, this means pressing ctrl+C terminates the container.
This can thus be omited, meaning containers are stopped by the `docker stop <container_name>` instead.

- List installed images: `docker images`
- List running containers: `docker ps`.
