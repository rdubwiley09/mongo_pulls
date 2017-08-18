from pymongo import MongoClient
from bson.son import SON
from bson.json_util import dumps
import urllib.parse
import pandas as pd

def get_city_voter_file(city):
    client = MongoClient('35.193.71.79',27017)
    db = client.get_database('new_voters')
    voter_file = db.voter_file
    election_history = db.election_history

    pipeline = [
        {
          "$match": {
            "city":city.upper()
          }
        },
        {
          "$lookup": {
              "from": "county_codes",
              "localField": "county_code",
              "foreignField": "county_code",
              "as": "county_info"
          }
        },
        {
          "$unwind": "$county_info"
        },
        {
          "$lookup": {
              "from": "jurisdiction_codes",
              "localField": "jurisdiction",
              "foreignField": "jurisdiction_code",
              "as": "jurisdiction_info"
          }
        },
        {
          "$unwind": "$jurisdiction_info"
        },
        {
          "$lookup": {
              "from": "appended_election_history",
              "localField": "voter_id",
              "foreignField": "voter_id",
              "as": "voter_history"
          }
        }
    ]

    with open('southfield.json', 'w') as f:
        f.write('')
    count = db.voter_file.find({"city":city.upper()}).count()
    aggregation = db.voter_file.aggregate(pipeline)
    for i, row in enumerate(aggregation):
        print("Running %s of %s" %(str(i),str(count)))
        with open('%s.json' %(city.lower()), 'a') as f:
            f.write(dumps(row)+"\n")
        f.close()

get_city_voter_file("southfield")
