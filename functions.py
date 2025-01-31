import time 
import math
import pathlib
from pydub import AudioSegment
from faster_whisper import WhisperModel
supported_filetypes = [".m4a",".mp3",".webm",".mp4",".mpga",".wav",".mpeg",]
#custom exception for when a file is opened with an unsupported filetype.
class UnsupportedFileType(Exception):
    def __init__(self, message):            
        super().__init__(message)
            
class time_stamp:
    '''Class to store data for each timestamp.'''
    def __init__(self,start,end,word,confidence,bias):
        self.start = start * 1000 #the start and end are multiplied into milliseconds to be compatible with pydub
        self.end = end * 1000
        self.word = word
        self.confidence = round(confidence,2)

def get_timestamps(audio,bias,model_size):
    """Creates and returns a list of timestamps for the given audio file."""
    #supported filetype check
    if get_filetype(audio) not in supported_filetypes:
        raise UnsupportedFileType(f"Audio file given uses unsupported file format {pathlib.Path(audio).suffix}")
    #load whisper
    model = WhisperModel(model_size)
    segments, _ = model.transcribe(audio, word_timestamps="word")
    words = []
    #Create a timestamp for each segment using the timestamp class and add it to a list.
    for segment in segments:
        for word in segment.words:
            words.append(time_stamp(word.start,word.end,word.word,word.probability,bias))
    #return the list
    return words

def get_segments(audio,file_format,bias,model_size="medium"):
    '''Creates files for the given audio in the provided file format'''

    #Open the given file with pydub
    segment = AudioSegment.from_file(audio,get_filetype(audio).replace(".",""))
    #create a list of timestamps
    timestamps = get_timestamps(audio,bias,model_size)
    #go through each timestamp in the list
    for timestamp in timestamps:
        #Slice and export each timestamp.
        slice = segment[timestamp.start:timestamp.end]
        slice.export(f"./segments/{timestamp.word} {timestamp.confidence}.{file_format}", format=f"{file_format}")

def convert_to_wav(input_file):
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format = "wav")
        return output_file
        
    
def diarize(audio):
    pass
def get_filetype(name):
    return pathlib.Path(name).suffix
get_segments("tests/Link _ The Faces of Evil - Intro (English) (HD 1080i).mp4","mp4",200)
