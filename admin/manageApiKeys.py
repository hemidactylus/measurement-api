#!/bin/env python

"""
    manageApiKeys.py
        We prefer to keep all functions in dbAccess 'API-ready' and async.
        "This is just an admin script", likely to be replaced by dedicated
        endpoints. So we shoehorn the imported functions to run 'synchronously'
        in the script by explicit control of the async event loop.
"""

import asyncio
import argparse

from api.database.dbAccess import createAPIKey, revokeAPIKey, session


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('command', help='Command to execute',
                        choices=['create', 'revoke'])
    parser.add_argument('customerID', help='Customer ID to act upon')
    parser.add_argument('rate',
                        help='Total time-window rate (used when creating)',
                        type=int, default=None, nargs='?')
    args = parser.parse_args()
    #
    if args.command == 'create':
        if args.rate is None:
            print('ERROR: when creating an API Key, please provide rate.')
        else:
            print('Creating API key for "%s" ... ' % args.customerID)
            loop = asyncio.get_event_loop()
            creCoro = createAPIKey(args.customerID, args.rate, session)
            result = loop.run_until_complete(creCoro)
            print('Key "%s" created for "%s".' % (result, args.customerID))
    else:
        print('Revoking API key for "%s" ... ' % args.customerID)
        loop = asyncio.get_event_loop()
        revCoro = revokeAPIKey(args.customerID, session)
        result = loop.run_until_complete(revCoro)
        print('Key for "%s" revoked.' % args.customerID)
