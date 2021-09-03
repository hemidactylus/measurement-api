"""
    dbAccess.py
"""

import datetime
from fastapi import HTTPException
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

from api.helpers.keyCreation import generateRandomKey

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


async def countHitsForCaller(caller, dbSession):
    #
    hitCountCQL = "SELECT COUNT(*) FROM requests WHERE caller_id=%s AND timestamp > %s;"
    oneHourAgo = datetime.datetime.now() - datetime.timedelta(hours=1)
    results = dbSession.execute(hitCountCQL, (caller.callerID, oneHourAgo))
    #
    return results[0].count


async def logRequest(caller, text, dbSession):
    return dbSession.execute(
        'INSERT INTO requests (caller_id, timestamp, text) VALUES (%s, %s, %s) USING TTL %s;',
        (caller.callerID, datetime.datetime.now(), text, getSettings().rateLimitWindowSeconds),
    )


async def checkTotalHits(caller, dbSession):
    if caller.anonymous:
        return getSettings().anonymousRateAllowed
    else:
        customerFindCQL = "SELECT api_key, rate_total FROM customers WHERE caller_id = %s;"
        results = list(dbSession.execute(customerFindCQL, (caller.callerID,)))
        if len(results) > 0:
            # API Key validation
            if caller.APIKey != results[0].api_key:
                raise HTTPException(401, 'Wrong API Key.')
            else:
                return results[0].rate_total
        else:
            raise HTTPException(401, 'Unknown customer ID.')


async def createAPIKey(callerID, rateTotal, dbSession):
    """
        Warning: will overwrite previous key for callerID, if any.
    """
    newKey = generateRandomKey()
    dbSession.execute(
        'INSERT INTO customers (caller_id, api_key, rate_total) VALUES (%s, %s, %s);',
        (callerID, newKey, rateTotal),
    )
    return newKey


async def revokeAPIKey(callerID, dbSession):
    dbSession.execute(
        'DELETE FROM customers WHERE caller_id = %s;',
        (callerID,),
    )
