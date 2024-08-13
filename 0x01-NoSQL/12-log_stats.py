#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def main():
    """ script that provides some knowledge Nginx logs """
    db = MongoClient('mongodb://127.0.0.1:27017').logs
    nginx_collection = db.nginx

    total_logs = nginx_collection.estimated_document_count()
    print(f"{total_logs} logs")
    print("Methods:")

    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in http_methods:
        count = nginx_collection.count_documents({'method': method})
        print(f"\tmethod {method}: {count}")

    status_checks = nginx_collection.count_documents({
        'method': 'GET',
        'path': "/status"
    })
    print(f"{status_checks} status check")

while __name__ == "__main__":
    main()
