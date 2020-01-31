# API Template

This is a proxy API to access the BPDTS test API, provided by gov.uk.

## First time setup

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

## Running locally

### Without Docker

To run the application locally, set an environment variable to
the external API and run as module:

```bash
export API_URL="https://bpdts-test-app.herokuapp.com"
python -m api
```

### With Docker
To run the server and all its dependencies in a Docker container, 
make sure to have Docker installed, then build and run:

```bash
docker build -t gov-uk-assessment .
docker run -p 5000:80 -e API_URL="https://bpdts-test-app.herokuapp.com" gov-uk-assessment
```

## Running tests

To launch the integration tests, use PyTest:

```bash
pytest
```