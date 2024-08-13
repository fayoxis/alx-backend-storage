#!/usr/bin/env python3
"""Module for retrieving schools by topic from a MongoDB collection."""

def schools_by_topic(mongo_collection, topic):
    """
    Retrieve schools with a specific topic from a MongoDB collection.

    Args:
        mongo_collection: MongoDB collection object
        topic (str): Topic to search for

    Returns:
        list: List of schools having the specified topic
    """
    if not mongo_collection:
        return []
    
    try:
        return list(mongo_collection.find({"topics": topic}))
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
