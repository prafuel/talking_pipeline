
import os
import torch
import torchaudio
from whisperspeech.pipeline import Pipeline

from config import config
from src.logger import get_logger

logger = get_logger()

if not os.path.exists(config.OUTPUT_FOLDER):
    os.mkdir(config.OUTPUT_FOLDER)

def TTS_whisperspeech(text: str, output_filename: str = None, speaker_url: str = None) -> str:
    """
    Convert text to speech using WhisperSpeech
    
    Args:
        text (str): Text to convert to speech
        output_filename (str, optional): Custom output filename
        speaker_url (str, optional): URL to speaker audio for voice cloning
    
    Returns:
        str: Path to the generated audio file
    """
    try:
        # Initialize WhisperSpeech pipeline
        logger.info("Loading WhisperSpeech model...")
        pipe = Pipeline(s2a_ref='collabora/whisperspeech:s2a-q4-tiny-en+pl.model')
        
        # Generate filename if not provided
        if output_filename is None:
            # Create safe filename from text (first 50 chars)
            safe_text = "".join(c for c in text[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_text = safe_text.replace(' ', '_')
            output_filename = f"tts_{safe_text}.wav"
        
        output_file = os.path.join(config.OUTPUT_FOLDER, output_filename)
        
        logger.info("Generating speech...")
        
        # Generate audio
        if speaker_url:
            # Use speaker reference for voice cloning
            logger.info(f"Using speaker reference: {speaker_url}")
            audio_tensor = pipe.generate(text, speaker=speaker_url)
        else:
            # Use default voice
            audio_tensor = pipe.generate(text)
        
        # Save audio file
        logger.info(f"Saving audio to: {output_file}")
        torchaudio.save(output_file, audio_tensor.cpu(), sample_rate=24000)
        
        logger.info(f"TTS audio file path: [{output_file}]")
        return output_file
        
    except Exception as e:
        logger.error(f"Error in TTS generation: {str(e)}")
        raise