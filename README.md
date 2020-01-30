# API Template

This is a proxy API to access the BPDTS test API, provided by gov.uk.

## Running with Docker
To run the server and all its dependencies in a Docker container,
and immediately start developing, please prepare your folder:

```bash
cp .env.example .env
```

You should add keys etc. to the .env file for external services.

Next, execute the following from the root directory:

```bash
docker-compose up
```

To see that it works, go to:

```
http://localhost/example/
```

## Running tests

You need to have Python 3.x installed, and you should consider 
setting up a virtual environment before progressing:

```bash
python3 -m venv venv
source venv/bin/activate
```

Make sure that you have all the necessary libraries installed:

```bash
pip install -r requirements.txt -r test-requirements.txt
```

To launch the integration tests, use PyTest:

```bash
pytest
```