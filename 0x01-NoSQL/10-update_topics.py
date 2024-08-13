#!/usr/bin/env python3
"""
Update school topics
"""
from pymongo.collection import Collection
from typing import List


def modify_subject_areas(collection: Collection, institution: str, subject_areas: List[str])
-> pymongo.results.UpdateResult:
    """
    Update multiple documents with new subject areas.

    Args:
        collection (Collection): MongoDB collection to operate on.
        institution (str): Name of the institution to update.
        subject_areas (List[str]): New list of subject areas to set.

    Returns:
        pymongo.results.UpdateResult: Result of the update operation.
    """
    update_query = {"name": institution}
    update_operation = {"$set": {"topics": subject_areas}}
    
    return collection.update_many(update_query, update_operation)
