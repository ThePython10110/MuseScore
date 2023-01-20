import os, json, subprocess, itertools, sys, argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-3", "--nomusescore3", help="Don't include MuseScore3 folder")
arg_parser.add_argument("-4", "--nomusescore4", help="Don't include MuseScore4 folder")
arg_parser.add_argument("-o", "--output", help="Output folder")
arg_parser.add_argument("-a", "--auto", help="Automatic (GitHub Actions)")
arg_parser.add_argument("-f", "--full", help="Full convert, ignore date checking")
args = arg_parser.parse_args()


filetypes = ["MP3", "MIDI", "PDF", "MSCX", "MXL", "MusicXML"]       # https://musescore.org/en/handbook/3/command-line-options#Batch_conversion_job_JSON_format for a list of file types

json_output = {"3":[],"4":[]}

folders=[]

if not args.nomusescore3:
    folders.append("MuseScore3")
if not args.nomusescore4:
    folders.append("MuseScore4")
if not folders:
    print("Nothing to scan!")
    
print("Scanning files...")
    

for root, dirs, files in itertools.chain(*[os.walk(folder) for folder in folders]):
    for name in files:                                              #For every file:
        if name.endswith(".mscz") and "Private" not in root:        #If it's a .mscz file and not in any folder called "Private"
            print(f"\tScanning {root}\\{name}")
            version = root[9]                                       #Should be "3" or "4"
            no_extension = name[:-5]                                #Get the filename without an extension (since I know the extension is ".mscz", I can just grab everything but the last 5 characters)
            path = os.path.join(root, name)                         #The path to the file (MuseScore4\HFF\Tomorrow.mscz for example)
            filenames = []
            score_modified = os.path.getmtime(path)                 #Get the time the score was modified
            for filetype in filetypes:                              #For every filetype:
                if args.output:
                    new_dir = root.replace("MuseScore" + version, output + "\\" + filetype, 1)
                else:
                    new_dir = root.replace("MuseScore" + version, filetype, 1)   #Replace the first instance of "MuseScore3" or "MuseScore4" in the path with the filetype (MuseScore4\HFF would become PDF\HFF, for example)
                if not os.path.exists(new_dir):                     #If the folder doesn't exist:
                    os.makedirs(new_dir)                            #Create it.
                new_filename = os.path.join(new_dir, no_extension + "." + filetype.lower()) #Generate the new file path (such as PDF\HFF\Tomorrow.pdf)
                if not args.full:
                    try:
                        file_modified = os.path.getmtime(new_filename)  #Get the modify date of the converted file
                    except FileNotFoundError:                           #The file may not exist yet
                        file_modified = 0                               #Setting this to zero, so if the file doesn't exist, it will assume it was modified at the epoch date
                    if score_modified > file_modified:                  #If the score has been modified since the last conversion:
                        filenames.append(new_filename)                  #Add it to the list of files to convert
                        print(f"\t\tAdding {new_filename} to list of filenames")
                else:
                    filenames.append(new_filename)
            if filenames:                                           #If there is anything to convert:
                json_output[version].append({                       #Add it to the JSON output
                    "in": path,
                    "out": filenames
                })

print("\nChecking for duplicates...")


if not args.nomusescore3 and not args.nomusescore4:
    for score in json_output["3"]:
        modified_score = {"in": score["in"].replace("MuseScore3", "MuseScore4"), "out": score["out"]}
        if modified_score in json_output["4"]:
            print(f"\tDuplicate score {modified_score['in']} detected, using MuseScore 4 version.")
            json_output["3"].remove(score)

print("\nWriting JSON files...")

if not args.nomusescore3:
    with open("convert_job3.json", "w") as json_file:                    #Write to the JSON file
        json.dump(json_output["3"], json_file, indent=2)
        print("\nConverting MuseScore 4 scores (takes several minutes)...")
        subprocess.call(r'"C:\Program Files\MuseScore 3\bin\MuseScore3.exe" -j convert_job3.json') #Convert!

if not args.nomusescore4:
    with open("convert_job4.json", "w") as json_file:                    #Write to the JSON file
        json.dump(json_output["4"], json_file, indent=2)
        print("\nConverting MuseScore 4 scores (takes several minutes)...")
        subprocess.call(r"""cmd -c '"C:\Program Files\MuseScore 4\bin\MuseScore4.exe" -j convert_job4.json'""") #Convert!

print("\nFlipping MIDI files...")

try:
    subprocess.call(r'midiflip.cmd -i "'+ (output if output else '.') + '/MIDI/**/*.midi" -o ' + (output if output else '.') + '"/FlippedMIDI"') #Flip all MIDI files, using https://github.com/1j01/midiflip
except FileNotFoundError:
    print("Midiflip is not on PATH.")
    try:
        subprocess.call(r'%UserProfile%\\node_modules\\.bin\\midiflip.cmd -i "'+ (output if output else '.') + '/MIDI/**/*.midi" -o ' + (output if output else '.') + '"/FlippedMIDI"') #Flip all MIDI files, using https://github.com/1j01/midiflip
    except FileNotFoundError:
        print("Midiflip is not installed. Install it with NodeJS with npm install midiflip\n\nIt should install to %UserProfile%\\node_modules\\.bin\\midiflip.cmd")

if not args.auto:
    input("\n(Press ENTER to exit)")
