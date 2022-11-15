import os, json

filetypes = ["MP3", "MIDI", "PDF"]

json_data = []
for root, dirs, files in os.walk("MuseScore"):
    for name in files: 
        if name.endswith(".mscz") and "Private" not in root: #I'm not making EVERYTHING public... :)
            no_extension = name[:-5]
            path = os.path.join(root, name)
            filenames = []
            for filetype in filetypes:
                new_dir = root.replace("MuseScore", filetype, 1)
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
                new_filename = os.path.join(new_dir, no_extension + "." + filetype.lower())
                filenames.append(new_filename)
            json_data.append({
                "in": path,
                "out": filenames
            })


print(json_data)
with open("convert_job.json", "w") as json_file:
    json.dump(json_data, json_file)
