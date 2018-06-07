"""
Coercion methods for cerberus validation.
"""

FLOAT_COERCER = lambda x: None if not x else int(x)
INT_COERCER = lambda x: None if not x else int(x)
