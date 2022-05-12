
import json
from urllib.request import urlopen
import os
from os import listdir


def download_entries(store_path, id):
    url_events = f"https://oris.orientacnisporty.cz/API/?format=json&method=getEventEntries&eventid={id}"
    response = urlopen(url_events)
    data_json = json.loads(response.read())
    with open(store_path, 'w') as outfile:
        json.dump(data_json["Data"], outfile)


def download_startlists(store_path, id):
    url_events = f"https://oris.orientacnisporty.cz/API/?format=json&method=getEventStartLists&eventid={id}"
    response = urlopen(url_events)
    data_json = json.loads(response.read())
    with open(store_path, 'w') as outfile:
        json.dump(data_json["Data"], outfile)


def download_classes(store_path, id):
    url_events = f"https://oris.orientacnisporty.cz/API/?format=json&method=getEvent&id={id}"
    response = urlopen(url_events)
    data_json = json.loads(response.read())
    with open(store_path, 'w') as outfile:
        json.dump(data_json["Data"], outfile)

def download_all_data(id):
    target_dir = os.path.join(os.path.dirname(__file__), id)
    if not os.path.isdir(target_dir):
        raise Exception(f"{target_dir} does not exist")

    entries_filename = os.path.join(target_dir, "entries.json")
    download_entries(entries_filename, id)

    startlists_filename = os.path.join(target_dir, "startlists.json")
    download_startlists(startlists_filename, id)

    classes_filename = os.path.join(target_dir, "event_info.json")
    download_classes(classes_filename, id)