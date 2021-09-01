"""
    algebra.py
"""

def factorMultiply(f1, f2):
    return (
        f1[0] * f2[0],
        {
            un: ue
            for un, ue in {
                u: f1[1].get(u, 0) + f2[1].get(u, 0)
                for u in f1[1].keys() | f2[1].keys()
            }.items()
            if ue != 0
        }
    )


def factorPower(f, exponent):
    return [
        f[0] ** exponent,
        {u: n * exponent for u, n in f[1].items()}
    ]
