# MuseScores

[![Automatic Batch Conversion](https://github.com/ThePython10110/MuseScore/actions/workflows/batch-convert.yml/badge.svg)](https://github.com/ThePython10110/MuseScore/actions/workflows/batch-convert.yml)

My MuseScore scores, also available [here](https://www.musescore.com/thepython10110).

Since MuseScore doesn't allow you to download files without a Pro account, I've decided to make mine publicly available on GitHub. I used Python and GitHub Actions to automatically convert them into several formats every time I push to this repository. Here's the [GitHub Actions YAML file](https://github.com/ThePython10110/MuseScore/blob/master/.github/workflows/batch-convert.yml), and here's the [Python script](https://github.com/ThePython10110/MuseScore/blob/master/batch_convert.py). The converted files are (fairly obviously) in the "Converted" folder.

The Python script is designed to be run in a folder with subfolders called MuseScore3 and MuseScore4, each containing scores from those versions. It doesn't include MuseScore 2 because I'm lazy. It also expects MS3 and MS4 to be installed on the default paths: `C:\Program Files\MuseScore #\bin\MuseScore#.exe` (where # is the major version number). The MIDI flipping capabilities rely on [my version](https://github.com/thepython10110/midiflip) of [midiflip](https://github.com/1j01/midiflip).

The GitHub Actions workflow runs on every push, unless the most recent commit includes "`|NoConvert|`" in the title. I will probably not rely on it much because I'd prefer to convert files on my computer so the VST plugins work correctly.

If you're going to distribute the scores, just make sure to give me (ThePython or ThePython10110) proper credit.
