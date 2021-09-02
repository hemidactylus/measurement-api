"""
    test_analyzer.py
"""

import pytest

from dimLib.formatting import dress
from dimLib.analyzer import validate

from dimLib.units import derivedUnits, fundamentalUnits, unitSynonyms


def test_validate():
    assert(dress(validate('1 m'))['label'] == '1 m')


def test_units_consistency():

    assert len(derivedUnits.keys() & fundamentalUnits) == 0, 'Overlap between fundamental and derived units'
        

    allOriginals = derivedUnits.keys() | fundamentalUnits
    assert len(unitSynonyms.keys() - allOriginals) == 0, 'Unknown symbols in the synonym list'

    allSynonymsList = [syn for syns in unitSynonyms.values() for syn in syns]
    allSynonyms = set(allSynonymsList)
    assert len(allSynonymsList) == len(allSynonyms), 'Duplicate synonyms detected'

    assert len(allSynonyms & allOriginals) == 0, 'Overlap between synonyms and original symbols'

    allMappingSymbols = {
        sym
        for origUnit in derivedUnits.values()
        for sym in origUnit[1].keys()
    }
    assert len(allMappingSymbols - fundamentalUnits) == 0, 'Not all units in mapping lead to fundamental units only'
