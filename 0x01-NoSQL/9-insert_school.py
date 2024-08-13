#!/usr/bin/env python3
"""Module for Task 9"""


def insert_school(mongo_collection, **kwargs):
    """
    Python function that inserts a new document in a collection based on kwargs.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection to insert into.
        **kwargs: The key-value pairs to be inserted as a document.

    Returns:
        str or None: The inserted document's ID if successful, otherwise None.
    """
    while mongo_collection is None:
        return None

    try:
        result = mongo_collection.insert_one(kwargs)
        return result.inserted_id
    except Exception as e:
        print("An error occurred:", str(e))
        return None
