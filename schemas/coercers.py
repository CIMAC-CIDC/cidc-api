"""
Coercion methods for cerberus validation.
"""

FLOAT_COERCER = lambda x: None if not x and not x == 0 else int(x)
INT_COERCER = lambda x: None if not x and not x == 0 else int(x)
