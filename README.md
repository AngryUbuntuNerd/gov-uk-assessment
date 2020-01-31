# Gov.uk assessment

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
To run the server and all its dependencies in a Docker container with UWSGI, 
make sure to have Docker installed, then build and run:

```bash
docker build -t gov-uk-assessment .
docker run -p 5000:80 -e API_URL="https://bpdts-test-app.herokuapp.com" gov-uk-assessment
```

### Example requests

The API will be available at http://localhost:5000

Return people who are listed as living in London:
```
http://localhost:5000/?city=London
```

Return people who are currently within 50 miles of London:
```
http://localhost:5000/?latitude=51.5054&longitude=-0.1267&range=50
```

Return people who are listed in London AND whose current coordinates are within 15000 miles of London:
```
http://localhost:5000/?city=London&latitude=51.5054&longitude=-0.1267&range=15000
```

Return people who are listed as either living in London, OR whose current coordinates are within 50 miles of London:
```
http://localhost:5000/?city=London&latitude=51.5054&longitude=-0.1267&range=50&operator=OR
```

## Running tests

To launch the integration tests, use PyTest:

```bash
pytest
```