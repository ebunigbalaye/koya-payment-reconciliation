#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

total = 0.0
count = 0
latest_events = {}   # dict to store the latest event for each txn_id


with open(r"payments.jsonl") as f:
    for line in f:
        try: #try block to catch JSON decoding errors i.e "lines that can't be read"
            event = json.loads(line)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from line: {line}")
            continue


        txn_id = event.get("txn_id")
        if txn_id is None: #if block to skip events with without a txn_id
            print(f"Skipping event with missing txn_id: {event}")
            continue

        event_timestamp = event["ts"]  #getting the event's timestamp
        prev = latest_events.get(txn_id)  #checking if we already have an event for this txn_id
        if prev is None or event_timestamp >= prev["ts"]: #if we don't have an event for this txn_id or if the current event is more recent than the previous one, we update the latest_events dictionary
                    latest_events[txn_id] = event  


for event in latest_events.values():  #looping through the latest events for each txn_id and adding up the amounts for successful payments
     if event["status"] == "success".lower():
            total +=  float(str(event["amount"]).replace(",", ""))
            count += 1


with open(r"expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")

