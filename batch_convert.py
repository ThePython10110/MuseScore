import os, json, subprocess

filetypes = ["MP3", "MIDI", "PDF"]

json_output = []

with open("last_changed.json", "r") as json_file:
    old_changes = json.load(json_file)

new_changes = old_changes

for root, dirs, files in os.walk("MuseScore"):
    for name in files: 
        if name.endswith(".mscz") and "Private" not in root: #I'm not making EVERYTHING public... :D
            no_extension = name[:-5]
            path = os.path.join(root, name)
            last_modified = os.path.getmtime(path)
            try:
                if last_modified != old_changes[no_extension]:
                    new_changes[no_extension] = last_modified
                    filenames = []
                    for filetype in filetypes:
                        new_dir = root.replace("MuseScore", filetype, 1)
                        if not os.path.exists(new_dir):
                            os.makedirs(new_dir)
                        new_filename = os.path.join(new_dir, no_extension + "." + filetype.lower())
                        filenames.append(new_filename)
                    json_output.append({
                        "in": path,
                        "out": filenames
                    })
            except KeyError:
                new_changes[no_extension] = last_modified
                filenames = []
                for filetype in filetypes:
                    new_dir = root.replace("MuseScore", filetype, 1)
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                    new_filename = os.path.join(new_dir, no_extension + "." + filetype.lower())
                    filenames.append(new_filename)
                json_output.append({
                    "in": path,
                    "out": filenames
                })


with open("convert_job.json", "w") as json_file:
    json.dump(json_output, json_file)

with open("last_modified.json", "w+") as json_file:
    json.dump(new_changes, json_file)
