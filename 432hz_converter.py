from pydub import AudioSegment
from pytube import YouTube

import numpy as np
import os
import sys

def change_pitch(audio_segment, semitones):
    """Change the pitch of an audio segment by a specified number of semitones."""
    new_sample_rate = int(audio_segment.frame_rate * (2.0 ** (semitones / 12.0)))
    return audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(audio_segment.frame_rate)

def convert_440hz_to_432hz(input_path):
    """Convert an audio file from 440 Hz to 432 Hz."""
    # Load the audio file
    audio = AudioSegment.from_file(input_path)

    # Calculate the semitone shift
    semitone_shift = -0.317666536334
    audio_432hz = change_pitch(audio, semitone_shift)

    # Create output file path
    file_name, file_extension = os.path.splitext(input_path)
    output_path = f"conversions/{file_name}{file_extension}"

    # Export the converted audio file
    audio_432hz.export(output_path, format="mp3")
    return output_path

def download_from_youtube(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    destination = "."
    out_file = video.download(output_path=destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return os.path.split(new_file)[-1]

if __name__ == "__main__":
    url = sys.argv[1]
    mp3_file = download_from_youtube(url)
    output_path = convert_440hz_to_432hz(mp3_file)
    print(f"File has been converted and saved to: {output_path}")
