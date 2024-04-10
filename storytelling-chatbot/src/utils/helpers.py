import os
import wave


def load_sounds(sound_files):
    sounds = {}
    script_dir = os.path.dirname(__file__)

    for file in sound_files:
        # Build the full path to the sound file
        full_path = os.path.join(script_dir, "../assets", file)
        # Get the filename without the extension to use as the dictionary key
        filename = os.path.splitext(os.path.basename(full_path))[0]
        # Open the sound and convert it to bytes
        with wave.open(full_path) as audio_file:
            sounds[filename] = audio_file.readframes(-1)

    return sounds
