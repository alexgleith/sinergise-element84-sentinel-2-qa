#!/usr/bin/env python3

import csv
import gzip
import json
import os
import sys

import gzip

import boto3

s3 = boto3.resource("s3")


bucket = "sentinel-inventory"
manifest_key = (
    "sentinel-s2-l2a/sentinel-s2-l2a-inventory/2020-07-27T00-00Z/manifest.json"
)
tile_list = "africa-mgrs-tiles.csv.gz"

region = "ap-southeast-2"

# 41KKQ,41KKT
tiles = []
with gzip.open(tile_list) as f:
    tiles = set([x.strip().decode('utf-8') for x in f.readlines()])

def log(comment):
    sys.stdout.write(f"\r{comment}")


# Stolen from https://alukach.com/posts/parsing-s3-inventory-output
def list_keys(bucket, manifest_key):
    manifest = json.load(s3.Object(bucket, manifest_key).get()["Body"])
    for obj in manifest["files"]:
        gzip_obj = s3.Object(bucket_name=bucket, key=obj["key"])
        buffer = gzip.open(gzip_obj.get()["Body"], mode="rt")
        reader = csv.reader(buffer)
        for row in reader:
            yield row


count = 0
valid = 0
log_every = 1000

if __name__ == "__main__":
    with gzip.open("data/sinergise-tiles.list.gz", "wt") as text_file:
        for bucket, key, *rest in list_keys(bucket, manifest_key):
            if "tileInfo.json" in key:
                # Counting scenes
                count += 1
                if count % log_every == 0:
                    log(
                        f"Found {valid} African scenes out of {count} scenes checked..."
                    )
                c = key.split("/")
                tile = f"{c[1]}{c[2]}{c[3]}"
                # Only storing scenes in Africa
                if tile in tiles:
                    valid += 1
                    text_file.write(f"s3://{bucket}/{key}\n")

print(f"Found {valid} scenes in Africa out of {count} total")
