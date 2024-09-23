from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained("diarizer/config.yaml")

# apply pretrained pipeline
diarization = pipeline("tests/ZeldaCDI(Faces of Evil).wav",num_speakers=4)

# print the result
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
# start=0.2s stop=1.5s speaker_0
# start=1.8s stop=3.9s speaker_1
# start=4.2s stop=5.7s speaker_0
# ...