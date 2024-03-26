#!/usr/bin/env python3
"""
Python function that inserts a new document in a
collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    Python function that inserts a
    new document in a collection based on kwargs
    :return: the new _id
    """
    new_document = mongo_collection.insert_one(kwargs)
    return new_document.inserted_id
