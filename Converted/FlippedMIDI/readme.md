# Flipped MIDI files
	These are flipped versions of all the MIDI files. Basically, all the notes are inverted, so high notes become low notes and vice versa. After doing that, every channel is transposed to
approximately its original octave.

	I did all this with [my version of](https://thepython10110.github.io/midiflip) midiflip (here's [the original](https://1j01.github.io/midiflip)), which just adds the octave-remapping option.

	Note: Anything in channels 10 and 11 is ignored since those channels are usually used for drums. This makes anything that uses those channels for anything besides drums sound kind of terrible.
For example, in "Following Stanley," MuseScore decided that it would be a good idea to put the "Voice" instrument on one of those channels. I could probably fix it by just changing the MIDI channel in
MuseScore, but I'm lazy (plus I already typed all this and I don't want to waste it).