
from src.STT import STT_whisper
from src.TTS import TTS_whisperspeech

audio_file = "10_Second_Talks.mp3"

# Speech to Text
text = STT_whisper(audio_file_path=audio_file)

print(text)

# Text to Speech
TTS_whisperspeech(text)