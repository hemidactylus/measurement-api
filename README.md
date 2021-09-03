# Measurement API

"A sample FastAPI service to validate/normalize expressions of dimensionful quantities"

## Setup

### On local machine

Tested with Python 3.8.

Suggested using `virtualenv` to keep your dependencies neatly and hygienically:
then `pip install -r requirements.txt` (in particular, make sure that
`cassandra-driver` is installed, as opposed to `dse-driver`, to properly
access Astra DB).

Add the project's root directory to the Pythonpath, e.g. creating a file such as

    ~/.virtualenvs/measurementapi38/lib/python3.8/site-packages/custom_path.pth

containing the (expanded) project's root directory.

Run (locally) with
```
./local_run.sh
```
or an equivalent command which invokes `uvicorn`.

Please note that the above `local_run.sh` wrapper overwrites "production"
settings (rate limit values, time-window size) with dummy values for easy
testing.

### Astra DB

Database name: `measurements`, keyspace name: `measurement_api`.

## Sample requests

Anonymous call:
```
curl -s -XPOST \
  'http://localhost:8000/v1/measurement/validate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"text": "120130015748.0316 inches / hours * days"}' | python -mjson.tool
```

Authenticated call:
```
curl -s -XPOST \
  -H 'x-customer-id: abc' \
  -H 'x-api-key: 123' \
  'http://localhost:8000/v1/measurement/validate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"text": "120130015748.0316 inches / hours * days"}' | python -mjson.tool
```

Checking available hits, anonymous:
```
curl -s \
  'http://localhost:8000/v1/info/rate_available' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' | python -mjson.tool
```

Checking available hits, authenticated:
```
curl -s \
  -H 'x-customer-id: abc' \
  -H 'x-api-key: 123' \
  'http://localhost:8000/v1/info/rate_available' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' | python -mjson.tool
```

## Testing

Run `python -m pytest .` from the project's home directory.

Test coverage is sketchy at best (not the main goal of this sample API).
