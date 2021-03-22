"""
Create file with recommended items for each user
"""

import os
import json
import csv
import argparse
import logging
from ast import literal_eval
import requests
#import time

# requests module need to be installed
def query_for_user(user_id, host_url, engine_id):
    """Creates POST requests for recommendation"""
    h = {'Content-Type': 'application/json'}
    if user_id:
        d = {'user': user_id}
    else:
        d = {}
    url = os.path.join(host_url,"engines", engine_id, "queries")
    r = requests.post(url, data=json.dumps(d), headers=h)
    return r


def export_recommendations(input_file, results_file, host_url, engine_id):
    results = list()
    with open(input_file, newline='') as csv_file:
        data = list(csv.reader(csv_file))
    for item in data:
        user_id = item[1]
        r = query_for_user(user_id, host_url, engine_id)
        print(r)
        extract_rec = r.text
        extract_rec = literal_eval(extract_rec)
        extract_rec["user_id"] = user_id
        results.append(extract_rec)
        #time.sleep(1)
    with open(results_file, 'w+') as res_file:
        res_file.write(json.dumps(results))
    csv_file.close()
    res_file.close()
    logging.info("Recommendations saved!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Import sample data for Universal Recommender Engine")
    parser.add_argument('--engine_id', default='ecommerce_ur')
    parser.add_argument('--url', default="http://localhost:9090")
    parser.add_argument('--input_file', default="docker-persistence/harness/data/input_data/2019-Nov-sample-intersection-userid.csv")
    parser.add_argument('--output_file', default="docker-persistence/harness/data/ecommerce_test_recommendations.json")
    args = parser.parse_args()
    print(args)

    print("Start creating recommendations...")
    export_recommendations(args.input_file, args.output_file, args.url, args.engine_id)
