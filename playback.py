import sys
import re
import time
import mido
import rtmidi

notes = {
    "A0": 21, "A#0": 22, "Bb0": 22, "B0": 23,
    "C1": 24, "C#1": 25, "Db1": 25, "D1": 26, "D#1": 27, "Eb1": 27, "E1": 28, "F1": 29, "F#1": 30, "Gb1": 30, "G1": 31, "G#1": 32, "Ab1": 32, "A1": 33, "A#1": 34, "Bb1": 34, "B1": 35,
    "C2": 36, "C#2": 37, "Db2": 37, "D2": 38, "D#2": 39, "Eb2": 39, "E2": 40, "F2": 41, "F#2": 42, "Gb2": 42, "G2": 43, "G#2": 44, "Ab2": 44, "A2": 45, "A#2": 46, "Bb2": 46, "B2": 47,
    "C3": 48, "C#3": 49, "Db3": 49, "D3": 50, "D#3": 51, "Eb3": 51, "E3": 52, "F3": 53, "F#3": 54, "Gb3": 54, "G3": 55, "G#3": 56, "Ab3": 56, "A3": 57, "A#3": 58, "Bb3": 58, "B3": 59,
    "C4": 60, "C#4": 61, "Db4": 61, "D4": 62, "D#4": 63, "Eb4": 63, "E4": 64, "F4": 65, "F#4": 66, "Gb4": 66, "G4": 67, "G#4": 68, "Ab4": 68, "A4": 69, "A#4": 70, "Bb4": 70, "B4": 71,
    "C5": 72, "C#5": 73, "Db5": 73, "D5": 74, "D#5": 75, "Eb5": 75, "E5": 76, "F5": 77, "F#5": 78, "Gb5": 78, "G5": 79, "G#5": 80, "Ab5": 80, "A5": 81, "A#5": 82, "Bb5": 82, "B5": 83,
    "C6": 84, "C#6": 85, "Db6": 85, "D6": 86, "D#6": 87, "Eb6": 87, "E6": 88, "F6": 89, "F#6": 90, "Gb6": 90, "G6": 91, "G#6": 92, "Ab6": 92, "A6": 93, "A#6": 94, "Bb6": 94, "B6": 95,
    "C7": 96, "C#7": 97, "Db7": 97, "D7": 98, "D#7": 99, "Eb7": 99, "E7": 100, "F7": 101, "F#7": 102, "Gb7": 102, "G7": 103, "G#7": 104, "Ab7": 104, "A7": 105, "A#7": 106, "Bb7": 106, "B7": 107,
    "C8": 108
}
instruments = {
    "Acoustic Grand Piano": 0,"Bright Acoustic Piano": 1,"Electric Grand Piano": 2,
    "Honky-tonk Piano": 3,"Electric Piano 1": 4,"Electric Piano 2": 5,
    "Harpsichord": 6, "Clavi": 7, "Celesta": 8, "Glockenspiel": 9,
    "Music Box": 10, "Vibraphone": 11, "Marimba": 12,
    "Xylophone": 13,
    "Tubular Bells": 14,
    "Dulcimer": 15,
    "Drawbar Organ": 16,
    "Percussive Organ": 17,
    "Rock Organ": 18,
    "Church Organ": 19,
    "Reed Organ": 20,
    "Accordion": 21,
    "Harmonica": 22,
    "Tango Accordion": 23,
    "Guitar (nylon)": 24,
    "Acoustic Guitar (steel)": 25,
    "Electric Guitar (jazz)": 26,
    "Electric Guitar (clean)": 27,
    "Electric Guitar (muted)": 28,
    "Overdriven Guitar": 29,
    "Distortion Guitar": 30,
    "Guitar harmonics": 31,
    "Acoustic Bass": 32,
    "Electric Bass (finger)": 33,
    "Electric Bass (pick)": 34,
    "Fretless Bass": 35,
    "Slap Bass 1": 36,
    "Slap Bass 2": 37,
    "Synth Bass 1": 38,
    "Synth Bass 2": 39,
    "Violin": 40,
    "Viola": 41,
    "Cello": 42,
    "Contrabass": 43,
    "Tremolo Strings": 44,
    "Pizzicato Strings": 45,
    "Orchestral Harp": 46,
    "Timpani": 47,
    "String Ensemble 1": 48,
    "String Ensemble 2": 49,
    "SynthStrings 1": 50,
    "SynthStrings 2": 51,
    "Choir Aahs": 52,
    "Voice Oohs": 53,
    "Synth Voice": 54,
    "Orchestra Hit": 55,
    "Trumpet": 56,
    "Trombone": 57,
    "Tuba": 58,
    "Muted Trumpet": 59,
    "French Horn": 60,
    "Brass Section": 61,
    "SynthBrass 1": 62,
    "SynthBrass 2": 63,
    "Soprano Sax": 64,
    "Alto Sax": 65,
    "Tenor Sax": 66,
    "Baritone Sax": 67,
    "Oboe": 68,
    "English Horn": 69,
    "Bassoon": 70,
    "Clarinet": 71,
    "Piccolo": 72,
    "Flute": 73,
    "Recorder": 74,
    "Pan Flute": 75,
    "Blown Bottle": 76,
    "Shakuhachi": 77,
    "Whistle": 78,
    "Ocarina": 79,
    "Lead 1 (square)": 80,
    "Lead 2 (sawtooth)": 81,
    "Lead 3 (calliope)": 82,
    "Lead 4 (chiff)": 83,
    "Lead 5 (charang)": 84,
    "Lead 6 (voice)": 85,
    "Lead 7 (fifths)": 86,
    "Lead 8 (bass+lead)": 87,
    "Pad 1 (new age)": 88,
    "Pad 2 (warm)": 89,
    "Pad 3 (polysynth)": 90,
    "Pad 4 (choir)": 91,
    "Pad 5 (bowed)": 92,
    "Pad 6 (metallic)": 93,
    "Pad 7 (halo)": 94,
    "Pad 8 (sweep)": 95,
    "FX 1 (rain)": 96,
    "FX 2 (soundtrack)": 97,
    "FX 3 (crystal)": 98,
    "FX 4 (atmosphere)": 99,
    "FX 5 (brightness)": 100,
    "FX 6 (goblins)": 101,
    "FX 7 (echoes)": 102,
    "FX 8 (sci-fi)": 103,
    "Sitar": 104,
    "Banjo": 105,
    "Shamisen": 106,
    "Koto": 107,
    "Kalimba": 108,
    "Bag pipe": 109,
    "Fiddle": 110,
    "Shanai": 111,
    "Tinkle Bell": 112,
    "Agogo": 113,
    "Steel Drums": 114,
    "Woodblock": 115,
    "Taiko drum": 116,
    "Melodic Tom": 117,
    "Synth Drum": 118,
    "Reverse Cymbal": 119,
    "Guitar Fret Noise": 120,
    "Breath Noise": 121,
    "Seashore": 122,
    "Bird Tweet": 123,
    "Telephone Ring": 124,
    "Helicopter": 125,
    "Applause": 126,
    "Gunshot": 127
}

CLEAN_STRIP_CHARS = "\n\t\r"
CHORD_STRIP_CHARS = "}{"
MEASURE_DELIMITER = ';'
TIMING_DELIMITER = '.'
DEF_TIMING_NUMERATOR = 4
DEF_TIMING_DENOMINATOR = 4
TIMING_MODIFIER = 2
MAX_WAIT_TIME = 4

OUTPUT_PORT = 'Microsoft GS Wavetable Synth 0'
DEF_INSTRUMENT = "Flute"

def extractChords(measure):
    chord_tuples = []
    cursor = 0
    while cursor < len(measure):
        # Find { to begin the chord
        start = measure.find("{", cursor)
        if start > -1:
            # Find } to end the chord
            stop = measure.find("}", cursor) + 1
            if stop > -1:
                # Add tuple to the list and move cursor accordingly
                # Each tuple has the chord itself, start index, and stop index
                chord = measure[start:stop].strip(CHORD_STRIP_CHARS)
                chord_tuples.append((chord, start, stop))
                cursor = stop
            else:
                break
        else:
            break

    return chord_tuples

def getNotes(composition_string):
    note_tuples = [] # List of tuples (note value, note time)
    # Clean the composition string
    composition_string = composition_string.strip(CLEAN_STRIP_CHARS)
    # Get a list of all measures
    measures = composition_string.split(MEASURE_DELIMITER)
    # Convert list of measures into list of measure tuples
    for i in range(0, len(measures)):
        measure = measures[i].strip()
        # Extract chords from each measure, without modifying the measure
        chord_tuples = extractChords(measure)
        j = 0
        note = ""
        stop = len(measure)
        while j < stop:
            character = measure[j]
            if j == stop - 1:
                note += character
            # Check if the character isn't a whitespace
            if character == ' ' or j == stop - 1:
                # Append to note tuples note, timing
                note, timing = note.split(TIMING_DELIMITER)
                note_tuples.append((note, int(timing)))
                note = "" # Reset note string for next note
            elif character == '{':
                # Get individual notes in chord
                chord_notes, start, end = chord_tuples[0]
                chord_notes = chord_notes.split()
                for k in range(0, len(chord_notes)):
                    # Split each chord note into its note string and time
                    note, timing = chord_notes[k].split(TIMING_DELIMITER)
                    if k < len(chord_notes) - 1:
                        # This makes all the chord notes play simultaneously
                        timing = '0'
                    # Add each chord note as if it were its own note, with timing
                    note_tuples.append((note, int(timing)))
                # Pop the chord from the tuples list to potentially access
                # the next chord later on, if applicable
                chord_tuples.pop(0)
                note = ""
                # Move the measure counter to after the chord
                j = end
            else:
                # Add more to the string representation of the next note
                note += character

            j += 1

    return note_tuples # Return list of (note value, note time) tuples               

def interpretComp(composition):
    composition_string = None
    try: # Check to see if composition input is a text file
        with open(composition, "r", encoding="utf-8") as comp_file:
            composition_string = comp_file.read()
            print(composition_string)
    except:
        # Composition input is most likely a string
        composition_string = composition

    return getNotes(composition_string)
    
        # print("\nError: Could not read the composition input!\n")
        # return -1
    
def sleep(timing, timing_scheme):
    timing = float(timing / DEF_TIMING_DENOMINATOR * timing_scheme)
    time.sleep(timing)

def play(note_tuples, instrument):
    with open('music_output.txt', 'w', encoding="utf-8") as file: 
        for i in range(0, len(note_tuples)):
            entry = "Index " + str(i) + " : " + str(note_tuples[i]) + "\n"
            file.write(entry)

    outport = mido.open_output(OUTPUT_PORT)
    velocity = 64
    channel = 0
    mido_notes = [] # List of (note_on, timing, note_off) tuples
    outport.send(mido.Message(
        'program_change', program=instruments.get(instrument), channel=channel))

    note_msgs = {i : ([], []) for i in range(0, len(note_tuples) + MAX_WAIT_TIME * 2)}
    i = 0 # Iterate through note_tuples
    j = 0 # Iterate through note_msgs
    k = 0 # Offset from on_note in note_msgs to off_note in note_msgs
    while i < len(note_tuples):
        # Add the next note in the list of note tuples
        note, timing = note_tuples[i]
        on_notes = [mido.Message('note_on', note=notes.get(note),
                               velocity=velocity, channel=channel)]
        off_notes = [mido.Message('note_off', note=notes.get(note),
                                velocity=velocity, channel=channel)]
        # Add all the chord notes simultaneously
        while timing == 0:
            i += 1
            note, timing = note_tuples[i]
            on_notes.append(mido.Message('note_on', note=notes.get(note),
                               velocity=velocity, channel=channel))
            off_notes.append(mido.Message('note_off', note=notes.get(note),
                                velocity=velocity, channel=channel))
        k = timing
        off_msgs = note_msgs[j + k][1]
        off_msgs.extend(off_notes.copy())
        # Add the next note simultaneously with the chord notes
        if len(on_notes) > 1:
            i += 1
            note, timing = note_tuples[i]
            on_notes.append(mido.Message('note_on', note=notes.get(note),
                               velocity=velocity, channel=channel))
            off_notes = [mido.Message('note_off', note=notes.get(note),
                                velocity=velocity, channel=channel)]
        k = timing
        # Record all the added notes in the note_msgs dict
        on_msgs = note_msgs[j][0]
        on_msgs.extend(on_notes.copy())
        off_msgs = note_msgs[j + k][1]
        off_msgs.extend(off_notes.copy())

        i += 1
        j += k
    note_msgs = {key : value for key, value in note_msgs.items() if key <= j}    
    i = 0
    while i < len(note_msgs):
        note_on_msgs, note_off_msgs = note_msgs[i]
        for note_msg in note_off_msgs:
            outport.send(note_msg)
        for note_msg in note_on_msgs:
            outport.send(note_msg)
        sleep(1, TIMING_MODIFIER)

        i += 1
    with open('music_output.txt', 'a', encoding="utf-8") as file: 
        for i in range(0, len(note_msgs)):
            entry = "Index " + str(i) + " : " + str(note_msgs.get(i)) + "\n"
            file.write(entry)

def main():
    composition = None
    instrument = DEF_INSTRUMENT
    try:
        composition = sys.argv[1]
        if len(sys.argv) > 1:
            instrument = sys.argv[2]
    except:
        print("\nError! No composition file or text supplied!\n" +
          "Usage: playback.py <composition> <instrument--optional>")
        sys.exit(-1)                                          

    # Get list of (note, timing) tuples
    print("\nReading %s ...\n", composition)
    note_tuples = interpretComp(composition)
    play(note_tuples, instrument) # Play the notes

if __name__ == "__main__":
    main()