"""
Import ecommerce data for recommendation
"""
import csv
from datetime import datetime
import harness
import argparse
import pytz

def create_event(row, client):
    """Create input events for the recommender.
    Args:
        - row: list denoting a row in a pandas dataframe
        - client: harness client
    """
    event_time = datetime.strptime(row[1],"%Y-%m-%d %H:%M:%S+00:00").replace(tzinfo=pytz.utc)
    event = row[2]
    entity_id = row[8]
    target_id = row[3]
    client.create(
        event = event,
        entity_type="user",
        entity_id = str(entity_id),
        target_entity_type = "item",
        target_entity_id = str(target_id)
        #event_time=event_time
    )
    print("Event: {}, entity_id: {}, target_entity_id: {}".format(event, entity_id, target_id))


# add pandas for python in the docker image
def import_events(client, file, nr_events):
    count = 0
    with open(file, newline='') as csv_file:
        data = list(csv.reader(csv_file))
    for item in data:
        create_event(item, client)
        print("Event nr. {}".format(count))
        count += 1
    csv_file.close()
    print("%s events are imported." % count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Import sample data for Universal Recommender Engine")
    parser.add_argument('--engine_id', default='ecommerce_ur')
    parser.add_argument('--url', default="http://localhost:9090")
    parser.add_argument('--input_file', default="docker-persistence/harness/data/input_data/2019-Nov-TEST.csv")
    parser.add_argument('--nr_events', default=2)
    #parser.add_argument('--primary_event', default="purchase")
    args = parser.parse_args()
    print(args)

    client = harness.EventsClient(
        engine_id=args.engine_id,
        url=args.url,
        threads=5,
        qsize=500 # ,
        # user_id=args.user_id,
        # user_secret=args.secret
    )
    print("Importing events...")
    import_events(client, args.input_file, args.nr_events)

