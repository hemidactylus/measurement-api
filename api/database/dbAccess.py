"""
    dbAccess.py
"""

import datetime
from fastapi import HTTPException
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

from api.settings import getSettings

from configuration.config import secure_db_bundle_path, secrets_json_path


cloud_config = {
    'secure_connect_bundle': secure_db_bundle_path,
}
auth = json.load(open(secrets_json_path))

auth_provider = PlainTextAuthProvider(auth['clientID'], auth['clientSecret'])
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('measurement_api')


async def getDbSession():
    try:
        yield session
    finally:
        pass
        # we do not "cluster.shutdown()" here since session is re-used.


async def countHitsForCaller(callerID, dbSession):
    #
    hitCountCQL = "SELECT COUNT(*) FROM requests WHERE caller_id=%s AND timestamp > %s;"
    oneHourAgo = datetime.datetime.now() - datetime.timedelta(hours=1)
    results = dbSession.execute(hitCountCQL, (callerID, oneHourAgo))
    #
    return results[0].count


async def logRequest(callerID, text, dbSession):
    return dbSession.execute(
        'INSERT INTO requests (caller_id, timestamp, text) VALUES (%s, %s, %s) USING TTL %s;',
        (callerID, datetime.datetime.now(), text, getSettings().rateLimitWindowSeconds),
    )


async def checkTotalHits(callerID, callerAPIKey, dbSession):
    customerFindCQL = "SELECT api_key, rate_total FROM customers WHERE caller_id = %s;"
    results = list(dbSession.execute(customerFindCQL, (callerID,)))
    if len(results) > 0:
        # API Key validation
        if callerAPIKey != results[0].api_key:
            raise HTTPException(401, 'Wrong API Key.')
        else:
            return results[0].rate_total
    else:
        return getSettings().anonymousRateAllowed

