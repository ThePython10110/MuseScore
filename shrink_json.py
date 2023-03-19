import json
import os

if os.path.isfile(r"c:\Portable\MuseScore\tmp.json"):
    print("FILE EXISTS")
with open(r"C:\Portable\MuseScore\tmp.json", "r") as json_file:
    json_data = json.load(json_file)
del json_data["pngs"]
del json_data["svgs"]
with open(r"C:\Portable\MuseScore\tmp.json", "w") as json_file:
    json.dump(json_data, json_file)
