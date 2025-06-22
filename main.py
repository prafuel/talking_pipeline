
from src.STT import STT_fasterwhisper
from src.TTS import TTS_whisperspeech

audio_file = "10_Second_Talks.mp3"

# Speech to Text
# text = STT_whisper(audio_file)
text = STT_fasterwhisper(audio_file)

print(text)

# Text to Speech
TTS_whisperspeech(text)