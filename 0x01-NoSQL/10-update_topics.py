#!/usr/bin/env python3
''' Module for updating school topics in MongoDB '''


def update_topics(mongo_collection, name, topics):
    '''
    Update topics of a school document based on the school name.
    
    Args:
        mongo_collection: MongoDB collection object
        name (str): Name of the school
        topics (list): New list of topics to set
    '''
    if not mongo_collection:
        return
    
    try:
        result = mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
        )
        print(f"Modified {result.modified_count} document(s)")
    except Exception as e:
        print(f"Error updating topics: {e}")
