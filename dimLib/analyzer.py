"""
    analyzer.py
"""

from functools import reduce

from .exceptions import MeasurementParseError
from .units import synonymMap, units, pureOne


def validate(m_string: str):
    """
    Given a string supposed to express a measurement,
    parse it into a Measurement object - or fail with an appropriate error.
    """

    # we clean the input a bit and split it in sensible 'segments' for parsing
    segments = [
        p
        for p in m_string.replace('/', ' / ').replace(
            '**', '^').replace('*', ' ').split(' ')
        if p != ''
    ]

    # Handle division sign, if present (Note: at most one)
    n_divisions = segments.count('/')
    if n_divisions > 1:
        raise MeasurementParseError('Illegal multiple division signs.')
    else:
        def accumulateE(done, exp_sign, todo):
            if len(todo) < 1:
                return done
            else:
                head = todo[0]
                new_exp_sign = exp_sign if head != '/' else -exp_sign
                return accumulateE(
                    done + [new_exp_sign],
                    new_exp_sign,
                    todo[1:],
                )
        exp_signs = accumulateE([], +1, segments)

        # make each segment into a MFactor:
        #   taking overall exp_signs into account
        #   ignoring the '/' sign itself from this point
        mFactors = [
            factorPower(parseFactor(seg), esig)
            for seg, esig in zip(segments, exp_signs)
            if seg != '/'
        ]

        # folding the factors into a single dimensionful quantity
        result = reduce(factorMultiply, mFactors, pureOne)

        return result


def parseFactor(f_string: str):
    number = isPureNumber(f_string)
    if number is not None:
        return (number, {})
    else:
        # we assume this piece is a unit, possibly with a trailing '^exponent'

        # we split symbol and exponent (if any)
        if '^' in f_string:
            symbol = f_string.split('^')[0]
            exp_piece = f_string.split('^')[1]
            try:
                exponent = int(exp_piece)
            except ValueError:
                raise MeasurementParseError(
                    'Invalid exponent: "%s"' % exp_piece
                )
        else:
            symbol = f_string
            exponent = 1

        symbol1 = synonymMap.get(symbol, symbol)
        if symbol1 in units:
            return factorPower(units[symbol1], exponent)
        else:
            raise MeasurementParseError(f'Unknown unit: "{symbol1}"')


def isPureNumber(f_string: str):
    try:
        return float(f_string)
    except ValueError:
        return None


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
