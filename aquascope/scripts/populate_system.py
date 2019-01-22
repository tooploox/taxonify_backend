import csv
import os
from datetime import datetime

from pymongo import MongoClient
import fire


def correct_values(csv_row):
    def remap_values(value):
        if value == 'FALSE':
            return False
        elif value == 'TRUE':
            return True
        elif value == 'null':
            return None
        else:
            try:
                value = float(value)
                value = datetime.fromtimestamp(value)
            except ValueError:
                pass

            return value

    return {k: remap_values(v) for k, v in csv_row.items()}


def populate_system(metadata_csv, images_directory):
    mongo_connection_string = os.environ['MONGO_CONNECTION_STRING']
    mongo_client = MongoClient(mongo_connection_string)
    db = mongo_client.get_database()

    with open(metadata_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        documents = [correct_values(row) for row in reader]
        db.items.insert_many(documents)


if __name__ == '__main__':
    fire.Fire(populate_system)

