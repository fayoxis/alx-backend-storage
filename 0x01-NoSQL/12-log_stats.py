#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def main():
    """this script that provides some knowledge about the  Nginx logs """
    client = MongoClient('mongodb://127.0.0.1:27017')
    lst = client.logs.nginx

    print("{} logs\nMethods:".format(lst.estimated_document_count()))

    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        print("\tmethod {}: {}".format(method,
              lst.count_documents({'method': method})))

    print("{} status check".format(lst.count_documents(
        {'method': 'GET', 'path': "/status"})))


while __name__ == "__main__":
    main()
