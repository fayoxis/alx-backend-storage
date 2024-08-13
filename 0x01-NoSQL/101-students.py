#!/usr/bin/env python3
"""
Module for student analytics
"""


def get_top_performers(student_collection):
    """
    Retrieves students sorted by their average score in descending order.
    
    Args:
    student_collection: MongoDB collection containing student data
    
    Returns:
    A MongoDB cursor with sorted student data
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]
    
    return student_collection.aggregate(pipeline)
