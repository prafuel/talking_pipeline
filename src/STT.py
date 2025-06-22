import os
import librosa
import whisper
from faster_whisper import WhisperModel

from config import config
from src.logger import get_logger

logger = get_logger()

if not os.path.exists(config.OUTPUT_FOLDER):
    os.mkdir(config.OUTPUT_FOLDER)

def STT_whisper(audio_file_path: str) -> str:
    try:
        model = whisper.load_model("turbo")
        audio, sr = librosa.load(audio_file_path, sr=16000)

        logger.info("Transcribing audio...")
        result = model.transcribe(audio)

        output_file = f"{config.OUTPUT_FOLDER}/transcript_{audio_file_path}.txt"

        with open(output_file, "w") as f:
            f.write(result['text'].strip())

        logger.info(f"Transcript file path :  [{output_file}]")

        return result['text']
    
    except Exception as e:
        logger.error(f"Error in STT generation: {str(e)}")
        raise

def STT_fasterwhisper(audio_file_path: str) -> str:
    try:
        model = WhisperModel("medium")
        segments, info = model.transcribe(audio_file_path)

        text = ""
        for segment in segments:
            text = text + segment.text
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

        output_file = f"{config.OUTPUT_FOLDER}/transcript_{audio_file_path}.txt"

        with open(output_file, "w") as f:
            f.write(text.strip())

        logger.info(f"Transcript file path :  [{output_file}]")

        return text
    except Exception as e:
        logger.error(f"error in STT {e}")
        raise