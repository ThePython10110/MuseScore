import os, json, subprocess

filetypes = ["MP3", "MIDI", "PDF", "MSCX", "MXL", "MusicXML"]                   # https://musescore.org/en/handbook/3/command-line-options#Batch_conversion_job_JSON_format for a list of file types

json_output = []

for root, dirs, files in os.walk("MuseScore"):                      #For every item in the MuseScore folder:
    for name in files: #For every file:
        if name.endswith(".mscz") and "Private" not in root:        #If it's a .mscz file and not in any folder called "Private" (I'm not making EVERYTHING public... :D)
            no_extension = name[:-5]                                #Get the filename without an extension (since I know the extension is ".mscz", I can just grab everything but the last 5 character)
            path = os.path.join(root, name)                         #The path to the file (MuseScore\HFF\Tomorrow.mscz for example)
            filenames = []
            score_modified = os.path.getmtime(path)                 #Get the time the score was modified
            for filetype in filetypes:                              #For every filetype:
                new_dir = root.replace("MuseScore", filetype, 1)    #Replace the first instance of "MuseScore" in the path with the filetype (MuseScore\HFF would become PDF\HFF, for example)
                if not os.path.exists(new_dir):                     #If the folder doesn't exist:
                    os.makedirs(new_dir)                            #Create it.
                new_filename = os.path.join(new_dir, no_extension + "." + filetype.lower()) #Generate the new file path (such as PDF\HFF\Tomorrow.pdf)
                file_modified = 0                                   #Setting this to zero, so if the file doesn't exist, it will assume it was modified at the epoch date
                try:
                    file_modified = os.path.getmtime(new_filename)  #Get the modify date of the converted file
                except FileNotFoundError:                           #The file may not exist yet
                    pass
                if score_modified > file_modified:                  #If the score has been modified since the last conversion:
                    filenames.append(new_filename)                  #Add it to the list of files to convert
            if filenames:                                           #If there is anything to convert:
                json_output.append({                                #Add it to the JSON output
                    "in": path,
                    "out": filenames
                })


with open("convert_job.json", "w") as json_file:                    #Write to the JSON file
    json.dump(json_output, json_file, indent=2)

subprocess.call(r'"C:\Program Files\MuseScore 3\bin\MuseScore3.exe" -j convert_job.json') #Convert!

subprocess.call(r'midiflip.cmd -i "MIDI/**/*.midi" -o "FlippedMIDI"') #Flip all MIDI files, using https://github.com/1j01/midiflip
# Unfortunately, there's no easy way to keep the MIDI file in a reasonable octave. I know how I would implement this
# (but not specifically enough): Find the highest and lowest note of each instrument, then transpose the flipped version
# by octaves to get it as close as possible to the original range. If anyone knows of (or creates) a tool that does this,
# please let me know (via an issue, discussion, PR, whatever).
