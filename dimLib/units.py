"""
    units.py
"""

from .utils import deep_merge
from .algebra import factorMultiply


pureOne = [1, {}]

fundamentalUnits = {'Kg', 'm', 's', 'A', 'K', 'mol', 'cd'}


# Note: there is only one degree for temperature, and it's called Kelvin!
derivedUnits = {
    # proportional to SI units
    'g': (0.001, {'Kg': 1}),
    'oz': (0.02834952, {'Kg': 1}),
    'lb': (0.4535924, {'Kg': 1}),
    'in': (0.0254, {'m': 1}),
    'ft': (0.3048, {'m': 1}),
    'yd': (0.9144, {'m': 1}),
    'furlong': (201.168, {'m': 1}),
    'mile': (1609.344, {'m': 1}),
    'au': (149597870700, {'m': 1}),
    'ly': (9460730472580800, {'m': 1}),
    'pc': (30856775814671900, {'m': 1}),
    'minute': (60.0, {'s': 1}),
    'hour': (3600.0, {'s': 1}),
    'day': (86400.0, {'s': 1}),
    'week': (7 * 86400.0, {'s': 1}),
    'month': (30 * 86400.0, {'s': 1}),
    'year': (365 * 86400.0, {'s': 1}),
    # non-unitary exponents
    'acre': (4046.86, {'m': 2}),
    'hectare': (10000, {'m': 2}),
    'Hz': (1, {'s': -1}),
    # composite dimensions for most physical quantities (SI + other)
    'kmh': (1/3.6, {'m': 1, 's': -1}),
    'mph': (1609.344/3.6, {'m': 1, 's': -1}),
    'N': (1, {'Kg': 1, 'm': 1, 's': -2}),
    'J': (1, {'Kg': 1, 'm': 2, 's': -2}),
    'cal': (4.184, {'Kg': 1, 'm': 2, 's': -2}),
    'Cal': (4184, {'Kg': 1, 'm': 2, 's': -2}),
    'W': (1, {'Kg': 1, 'm': 2, 's': -3}),
    'hp': (745.7, {'Kg': 1, 'm': 2, 's': -3}),
    'Pa': (1, {'Kg': 1, 'm': -1, 's': -2}),
    'psi': (6895, {'Kg': 1, 'm': -1, 's': -2}),
    'bar': (100000, {'Kg': 1, 'm': -1, 's': -2}),
    'atm': (101325, {'Kg': 1, 'm': -1, 's': -2}),
    'torr': (133.32, {'Kg': 1, 'm': -1, 's': -2}),
    'inHg': (3376.85, {'Kg': 1, 'm': -1, 's': -2}),
    'T': (1, {'Kg': 1, 'A': -1, 's': -2}),
    'G': (0.0001, {'Kg': 1, 'A': -1, 's': -2}),
    'Wb': (1, {'Kg': 1, 'm': 2, 's': -2, 'A': -1}),
    'C': (1, {'A': 1, 's': 1}),
    'Ω': (1, {'Kg': 1, 'm': 2, 'A': -2, 's': -3}),
    'V': (1, {'Kg': 1, 'm': 2, 'A': -1, 's': -3}),
    'S': (1, {'Kg': -1, 'm': -2, 'A': 2, 's': 3}),
    'F': (1, {'Kg': -1, 'm': -2, 'A': 2, 's': 4}),
    'H': (1, {'Kg': 1, 'm': 2, 'A': -2, 's': -2}),
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

unitSynonyms = {
    'N': {'newton', 'newtons', 'Newton', 'Newtons'},
    'J': {'joule', 'joules', 'Joule', 'Joules'},
    'cal': {'calorie', 'calories'},
    'Cal': {'Calorie', 'Calories', 'kcal', 'Kcal'},
    'W': {'watt', 'Watt', 'Watts', 'watts'},
    'hp': {'horsepower', 'horsepowers'},
    'Pa': {'pascal', 'pascals', 'Pascal', 'Pascals'},
    'atm': {'atmosphere', 'atmospheres'},
    'torr': {'mmHg'},
    'T': {'Tesla', 'Teslas', 'tesla', 'teslas'},
    'G': {'Gs', 'gauss', 'Gauss'},
    'Wb': {'Weber', 'Webers', 'weber', 'webers'},
    'C': {'Coulomb', 'Coulombs', 'coulomb', 'coulombs'},
    'Ω': {'Ohm', 'ohm', 'ohms', 'Ohms'},
    'V': {'Volt', 'Volts', 'volt', 'volts'},
    'S': {'Siemens', 'siemens'},
    'F': {'Farad', 'Farads', 'farad', 'farads'},
    'H': {'Henry', 'Henrys', 'henry', 'henrys'},
    'g': {'gram', 'grams'},
    'oz': {'ounce', 'ounces'},
    'm': {'meter', 'meters'},
    'in': {'inch', 'inches'},
    'ft': {'foot', 'feet'},
    'yd': {'yard', 'yards'},
    'ly': {'light-year', 'light-years', 'lightyear', 'lightyears'},
    'pc': {'parsec', 'parsecs'},
    'day': {'days'},
    'minute': {'minutes', 'min', 'mins'},
    'hour': {'hours', 'hrs', 'hr'},
    'acre': {'ac', 'acres'},
    'hectare': {'ha', 'hectares'},
    'A': {'Ampere', 'Amperes', 'ampere', 'amperes'},
    'K': {'Kelvin', 'kelvin', 'Kelvins', 'kelvins'},
    'mol': {'mole', 'moles'},
    'cd': {'candela', 'candelas'},
}

autoDerivedUnitSeed = {
    'm': standardPrefixes,
    's': standardPrefixes,
    'A': standardPrefixes,
    'K': standardPrefixes,
    'mol': standardPrefixes,
    'cd': standardPrefixes,
    'Hz': standardPrefixes,
    'N': standardPrefixes,
    'J': standardPrefixes,
    'W': standardPrefixes,
    'T': standardPrefixes,
    'G': standardPrefixes,
    'Gs': standardPrefixes,
    'Wb': standardPrefixes,
    'C': standardPrefixes,
    'Ω': standardPrefixes,
    'V': standardPrefixes,
    'S': standardPrefixes,
    'F': standardPrefixes,
    'H': standardPrefixes,
}

units0 = {
    fu: [1, {fu: 1}]
    for fu in fundamentalUnits
}

units1 = deep_merge(
    units0,
    derivedUnits,
)

unitsFromSynonyms = {
    syn: units1[origUnit]
    for origUnit, syns in unitSynonyms.items()
    for syn in syns
}
units2 = deep_merge(
    units1,
    unitsFromSynonyms,
)

unitsWithPrefix = {
    '%s%s' % (prefixName, origUnit): factorMultiply(
        (prefixFactor, {}),
        units2[origUnit]
    )
    for origUnit, prefixMap in autoDerivedUnitSeed.items()
    for prefixName, prefixFactor in prefixMap.items()
}
units = deep_merge(
    units2,
    unitsWithPrefix,
)
