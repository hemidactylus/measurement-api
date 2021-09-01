"""
    exceptions.py
"""


class MeasurementParseError(Exception):
    """Occurs when a m_string cannot be parsed into a Measurement."""
    def __init__(self, name: str):
        self.name = name
