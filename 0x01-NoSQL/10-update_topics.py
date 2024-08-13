#!/usr/bin/env python3
''' Module for updating school topics in MongoDB '''
 import pymongo


def update_topics(mongo_collection, name, topics):
    '''
    Update topics of a school document based on the school name.
    
    Args:
        mongo_collection: MongoDB collection object
        name (str): Name of the school
        topics (list): New list of topics to set
    '''

    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
