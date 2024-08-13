#!/usr/bin/env python3
''' Module for updating school topics in a MongoDB collection '''

def update_topics(mongo_collection, name, topics):
    '''
    Updates the topics of a school document based on the school name.

    Args:
        mongo_collection: MongoDB collection object
        name (str): Name of the school to update
        topics (list): New list of topics to set for the school

    Returns:
        None
    '''
if mongo_collection is None:
        return
    
    try:
        mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
    except Exception as e:
        print("An error occurred:", str(e))
