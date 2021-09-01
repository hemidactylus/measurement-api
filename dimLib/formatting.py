"""
    formatting.py
"""

from operator import itemgetter
import math


def dress(measurement):
    stringDesc = describeMeasurement(measurement)
    return {
        'label': stringDesc,
        'measurement': measurement,
    }


def describeMeasurement(meas):
    numeric = meas[0]
    unitMap = {
        un: ue
        for un, ue in meas[1].items()
        if ue != 0
    }
    # number
    if abs(math.log(numeric, 10)) <= 4:
        if int(numeric) == numeric:
            number_string = '%i' % numeric
        else:
            number_string = '%.2f' % numeric
    else:
        number_string = '%.2e' % numeric

    # dimensions
    if len(unitMap) == 0:
        dimension_string = ''
    else:
        num_units = {un: ue for un, ue in unitMap.items() if ue > 0}
        den_units = {un: ue for un, ue in unitMap.items() if ue < 0}
        num_string = makeUnitsString(num_units, parens=False)
        if len(den_units) > 0:
            den_string = makeUnitsString(den_units, parens=True, invert=True)
            dimension_string = '%s / %s' % (num_string, den_string)
        else:
            dimension_string = num_string

    return ('%s %s' % (number_string, dimension_string)).strip()


def makeUnitsString(unitMap, parens, invert=False):
    unit_strings = [
        makeUnitString(un, ue if not invert else -ue)
        for un, ue in sorted(unitMap.items(), key=itemgetter(0))
    ]
    if parens and len(unit_strings) > 1:
        return '(%s)' % ' * '.join(unit_strings)
    else:
        return ' * '.join(unit_strings)


def makeUnitString(un, ue):
    if ue == 1:
        return un
    elif ue > 0:
        return '%s^%i' % (un, ue)
    else:
        return '%s^(%i)' % (un, ue)
