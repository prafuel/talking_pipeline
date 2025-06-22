import os
import librosa
import whisper

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