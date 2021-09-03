## TODOs

pep8 refresh

docstrings

helpful comments

rewrite flow anon/customer, all of it

logging/debug log

### Creation of tables:

To be automated:

```
USE measurement_api;

CREATE TABLE measurement_api.requests (
    caller_id TEXT,
    timestamp TIMESTAMP,
    text TEXT,
    PRIMARY KEY (caller_id, timestamp)
) WITH CLUSTERING ORDER BY (timestamp ASC);

CREATE TABLE customers (caller_id TEXT PRIMARY KEY, api_key TEXT, rate_total INT);
```
