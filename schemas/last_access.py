#!/usr/bin/env python
"""
Stores a user's last time touching the database.
"""
__author__ = "Lloyd McCarthy"
__license__ = "MIT"

from schemas.fielder import fielder

LAST_ACCESS = {
    "public_methods": [],
    "resource_methods": ["GET"],
    "allowed_roles": ["admin", "system"],
    "allowed_item_roles": ["admin", "system"],
    "schema": {},
}

LAST_ACCESS["schema"].update(
    [fielder("last_access"), fielder("email", unique=True)]
)
