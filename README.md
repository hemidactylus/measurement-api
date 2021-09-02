# Measurement API

"A sample FastAPI service to validate/normalize expressions of dimensionful quantities"

## Sample requests

curl -s -XPOST   'http://localhost:8000/v1/measurement/validate'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{"text": "m"}' | python -mjson.tool

curl -s -XPOST   'http://localhost:8000/v1/measurement/validate'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{"text": "120130015748.0316 inches / hours * days"}' | python -mjson.tool

python -m pytest .
