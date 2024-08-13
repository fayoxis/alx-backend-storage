#!/usr/bin/env python3
""" module for for the last task """
from pymongo import MongoClient

def main():
    """this  script will provides some stats about Nginx logs """
    client = MongoClient('mongodb://127.0.0.1:27017')
    lst = client.logs.nginx

    print("{} logs".format(lst.estimated_document_count()))
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    i = 0
    while True:
        if i >= len(methods):
            break
        method = methods[i]
        print("\tmethod {}: {}".format(method, lst.count_documents({'method': method})))
        i += 1

    print("{} status check".format(lst.count_documents({'method': 'GET', 'path': "/status"})))

    print("IPs:")
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    top_ips = list(lst.aggregate(pipeline))

    i = 0
    while i < len(top_ips):
        ip_info = top_ips[i]
        print("\t{}: {}".format(ip_info["_id"], ip_info["count"]))
        i += 1

if __name__ == "__main__":
    main()
