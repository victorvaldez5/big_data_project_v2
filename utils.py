import os
import json
from pprint import pprint
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.bills_database

'''
  Document Schema
  Bill:
    Official Title: String
    Short Title: String
    bill_id: String
    Action Count: Int
    Amendment Count: Int
    status: String
    house_pass: Boolean
    senate_pass: Boolean
    vetoed: Boolean
    enacted: Boolean
    subjects: List of Strings
    Main Subject: String
    Summary: String
'''
def fillBillsCollection(dataset):
  bills = db[f'bills_{dataset}']
  data = next(os.walk(os.path.join(os.getcwd(), f"{dataset}_data")))[2]
  for f in data:
    with open(os.path.join(os.getcwd(), f"{dataset}_data", f), "r") as bill:
      bill_dict = json.load(bill)
      official_title = bill_dict['official_title']
      short_title = bill_dict['short_title']
      bill_id = bill_dict['bill_id']
      action_count = len(bill_dict['actions'])
      amendment_count = len(bill_dict['amendments'])
      status = bill_dict['status']
      try:
        house_pass = bill_dict['history']['house_passage_result']
      except:
        house_pass = False
      try:
        senate_pass = bill_dict['history']['senate_passage_result']
      except:
        senate_pass = False
      vetoed = bill_dict['history']['vetoed']
      enacted = bill_dict['history']['enacted']
      subjects = bill_dict['subjects']
      main_subject = bill_dict['subjects_top_term']
      try:
        summary = bill_dict['summary']['text']
      except:
        summary = None
      bill_obj = {
        "official_title": official_title,
        "short_title": short_title,
        "bill_id": bill_id,
        "actions": action_count,
        "amendments": amendment_count,
        "status": status,
        "house_pass": house_pass,
        "senate_pass": senate_pass,
        "vetoed": vetoed,
        "enacted":enacted,
        "subjects": subjects,
        "main_subject": main_subject,
        "summary": summary
      }
      bills.insert_one(bill_obj)
      print(f"Bill {bill_obj['short_title']}({bill_obj['bill_id']}) has been inserted")



fillBillsCollection('114')
fillBillsCollection('113')
# for bill in data_list:



# deserialized = json.loads(data[0])
# print(deserialized)