#!/usr/bin/env python3
"""Module for listing top students in a MongoDB collection"""


def top_students(mongo_collection):
    """
    Function that retrieves the top students based on their average score.

    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection.

    Returns:
        list: A list of dictionaries, each representing a student with their
              name and average score.
    """
    pipeline = [
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ]

    return list(mongo_collection.aggregate(pipeline))
