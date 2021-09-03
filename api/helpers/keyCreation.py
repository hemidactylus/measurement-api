"""
    keyCreation.py
"""

import secrets

KEY_LENGTH = 24
KEY_ALPHABET = list('0123456789abcdefghijklmnopqrstuvABCDEFGHIJKLMNOPQRSTUV')


def generateRandomKey():
    return ''.join(
        secrets.choice(KEY_ALPHABET)
        for _ in range(KEY_LENGTH)
    )
