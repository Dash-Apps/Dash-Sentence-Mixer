import time 
import math
import pathlib
from pydub import AudioSegment
from faster_whisper import WhisperModel
supported_filetypes = [".m4a",".mp3",".webm",".mp4",".mpga",".wav",".mpeg",]
class UnsupportedFileType(Exception):
    def __init__(self, message):            
        super().__init__(message)
            
class time_stamp:
    def __init__(self,start,end,word,confidence):
        self.start = start *1000 - 50
        self.end = end * 1000 +50
        self.word = word
        self.confidence = round(confidence,2)
def get_timestamps(audio):
    if get_filetype(audio) not in supported_filetypes:
        raise UnsupportedFileType(f"Audio file given uses unsupported file format {pathlib.Path(audio).suffix}")
    model = WhisperModel('small')
    segments, _ = model.transcribe(audio, word_timestamps=True)
    words = []
    for segment in segments:
        for word in segment.words:
            words.append(time_stamp(word.start,word.end,word.word,word.probability))
    return words
def get_segments(audio):
    timestamps = get_timestamps(audio)
    for timestamp in timestamps:
        segment = AudioSegment.from_file(audio,get_filetype(audio).replace(".",""))
        slice = segment[timestamp.start:timestamp.end]
        slice.export(f"./segments/{timestamp.word} {timestamp.confidence}.mp3", format="mp3")

        
def get_filetype(name):
    return pathlib.Path(name).suffix
get_segments("narration.mp3")
