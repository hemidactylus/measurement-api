import os

this_dir = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.join(this_dir, '..')
secure_db_bundle_path = os.path.join(
    base_dir,
    'secrets',
    'secure-connect-measurements.zip',
)

secrets_json_path = os.path.join(
    base_dir,
    'secrets',
    'access.json',
)

defaultRateLimitWindowSeconds = 3600
defaultAnonymousRateAllowed = 50
