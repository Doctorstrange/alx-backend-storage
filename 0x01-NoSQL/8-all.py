#!/usr/bin/env python3
"""
function that lists all documents in a collection:
"""


def list_all(mongo_collection):
    """
    lists all documents in a collection
    :return: Return an empty list if no document in the collection
    """
    return mongo_collection.find()
