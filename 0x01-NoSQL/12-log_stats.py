#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def get_method_count(collection, method):
    return collection.count_documents({'method': method})

def main():
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx

    # Get number of documents in collection
    docs_num = nginx_logs.count_documents({})

    # Count documents for each HTTP method
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    method_counts = {method: get_method_count(nginx_logs, method) for method in methods}

    # Count GET requests to /status
    get_status = nginx_logs.count_documents({'method': 'GET', 'path': '/status'})

    # Print results
    print(f"{docs_num} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{get_status} status check")

if __name__ == "__main__":
    main()
