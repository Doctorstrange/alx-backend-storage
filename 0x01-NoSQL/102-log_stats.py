#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top
10 of the most present IPs in the collection
nginx of the database logs:
"""
from pymongo import MongoClient


def log_stats():
    """
    Improve 12-log_stats.py by adding the top
    10 of the most present IPs in the collection
    nginx of the database logs:
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    total = logs.count_documents({})
    get = logs.count_documents({"method": "GET"})
    post = logs.count_documents({"method": "POST"})
    put = logs.count_documents({"method": "PUT"})
    patch = logs.count_documents({"method": "PATCH"})
    delete = logs.count_documents({"method": "DELETE"})
    path = logs.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")
    print("IPs:")
    ips = logs.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    x = 0
    for s in ips:
        if x == 10:
            break
        print(f"\t{s.get('_id')}: {s.get('count')}")
        x += 1


if __name__ == "__main__":
    log_stats()
