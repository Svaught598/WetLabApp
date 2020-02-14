import json


def loader():
    with open("data.json") as f:
        return json.load(f)


def dumper(dict):
    json.dump(dict, open("data.json", "w"))