"""
    units.py
"""

from .utils import deep_merge


pureOne = [1, {}]

fundamentalUnits = {'Kg', 'm', 's'}

derivedUnits = {
    'g': (0.001, {'Kg': 1}),
    'oz': (0.02834952, {'Kg': 1}),
    'N': (1, {'Kg': 1, 'm': 1, 's': -2}),
    'in': (0.0254, {'m': 1}),
    'day': (86400.0, {'s': 1}),
    'hour': (3600.0, {'s': 1}),
    'minute': (60.0, {'s': 1}),
    'acre': (4046.86, {'m': 2}),
    'hectare': (10000, {'m': 2}),
    'Hz': (1, {'s': -1}),
}

standardPrefixes = {
    'Y': 10**24,
    'Z': 10**21,
    'E': 10**18,
    'P': 10**15,
    'T': 10**12,
    'G': 10**9,
    'M': 10**6,
    'K': 10**3,
    'm': 10**(-3),
    'micro': 10**(-6),
    'μ': 10**(-6),
    'n': 10**(-9),
    'p': 10**(-12),
    'f': 10**(-15),
    'a': 10**(-18),
    'z': 10**(-21),
    'y': 10**(-24),
}

autoDerivedUnitSeed = {
    'm': standardPrefixes,
    's': standardPrefixes,
    'N': standardPrefixes,
    'Hz': standardPrefixes,
}

unitSynonyms = {
    'g': {'gram', 'grams'},
    'oz': {'ounce', 'ounces'},
    'in': {'inch', 'inches'},
    'm': {'meter', 'meters'},
    'day': {'days'},
    'minute': {'minutes'},
    'hour': {'hours'},
    'acre': {'ac'},
    'hectare': {'ha'},
}

# TODO checks (uniqueness, non-overlaps, all in fct of fund units in deriveds)

# helper data structures - automatically generated from the above
synonymMap = {
    syn: uni
    for uni, syns in unitSynonyms.items()
    for syn in syns
}

autoDerivedUnits = {
    '%s%s' % (prefixName, origUnit): (prefixFactor, {origUnit: 1})
    for origUnit, prefixMap in autoDerivedUnitSeed.items()
    for prefixName, prefixFactor in prefixMap.items()
}

units = deep_merge(
    {
        fu: [1, {fu: 1}]
        for fu in fundamentalUnits
    },
    deep_merge(
        derivedUnits,
        autoDerivedUnits,
    ),
)
