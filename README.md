# MuseScores

[![Automatic Batch Conversion](https://github.com/ThePython10110/MuseScore/actions/workflows/batch-convert.yml/badge.svg)](https://github.com/ThePython10110/MuseScore/actions/workflows/batch-convert.yml)

My MuseScore scores, also available [here](https://www.musescore.com/thepython10110).

Since MuseScore doesn't allow you to download files without a Pro account, I've decided to make mine publicly available on GitHub. I used Python and GitHub Actions to automatically convert them into several formats every time I push to this repository. Here's the [GitHub Actions YAML file](https://github.com/ThePython10110/MuseScore/blob/master/.github/workflows/batch-convert.yml), and here's the [Python script](https://github.com/ThePython10110/MuseScore/blob/master/batch_convert.py). The converted files are (fairly obviously) in the "Converted" folder.

I may intentionally include `|NoConvert|` in some of my commit names to keep the conversion from running (because it really doesn't need to). I probably also need to convert the MuseScore 4 files locally on my computer, as several of them use VST plugins, so that could get complicated.

If you're going to distribute these, just make sure to give me (ThePython or ThePython10110) proper credit.
