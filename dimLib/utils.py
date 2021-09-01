"""
    utils.py
"""


def deep_merge(main, default):
    """
    Pure dict deep-merge function. First dict has precedence.
    """
    if isinstance(main, dict):
        return {
            k: deep_merge(
                main[k],
                default=({} if default is None else default).get(k),
            ) if k in main else default[k]
            for k in ({} if default is None else default.keys()) | main.keys()
        }
    else:
        return main
