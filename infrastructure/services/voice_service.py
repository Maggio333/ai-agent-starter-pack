"""
Voice Service - Business logic for STT and TTS
"""
import tempfile
import os
import logging
from pathlib import Path
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

# STT imports
try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None

# TTS imports  
try:
    import piper
    import soundfile as sf
except ImportError:
    piper = None
    sf = None

logger = logging.getLogger(__name__)

# Global models (singleton pattern)
_whisper_model = None
_piper_model = None


class VoiceService:
    """Service for voice processing (STT and TTS)"""
    
    def __init__(self):
        self.whisper_model = self._get_whisper_model()
        self.piper_model = self._get_piper_model()
    
    def _get_whisper_model(self) -> Optional[WhisperModel]:
        """Get or create Whisper model (singleton)"""
        global _whisper_model
        if _whisper_model is None and WhisperModel is not None:
            try:
                logger.info("Loading Whisper model...")
                # Use small model for faster processing
                _whisper_model = WhisperModel("small", device="cpu", compute_type="int8")
                logger.info("Whisper model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")
                logger.error(f"Exception type: {type(e)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                _whisper_model = None
        return _whisper_model
    
    def _get_piper_model(self) -> Optional[Any]:
        """Get or create Piper model (singleton)"""
        global _piper_model
        if _piper_model is None and piper is not None:
            try:
                logger.info("Attempting to load Piper model...")
                
                # Use local Polish voice model
                voice_path = Path("./voices/pl_PL-gosia-medium.onnx")
                config_path = Path("./voices/pl_PL-gosia-medium.onnx.json")
                
                logger.info(f"Voice path: {voice_path}")
                logger.info(f"Config path: {config_path}")
                logger.info(f"Voice exists: {voice_path.exists()}")
                logger.info(f"Config exists: {config_path.exists()}")
                
                if voice_path.exists() and config_path.exists():
                    logger.info("Loading Piper model...")
                    _piper_model = piper.PiperVoice.load(str(voice_path), str(config_path))
                    logger.info("Piper Polish voice model loaded successfully")
                    logger.info(f"Model config: {_piper_model.config}")
                else:
                    logger.warning("Polish voice model not found, using fallback")
                    _piper_model = None
            except Exception as e:
                logger.error(f"Failed to load Piper model: {e}")
                logger.error(f"Exception type: {type(e)}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                _piper_model = None
        return _piper_model
    
    async def transcribe_audio(self, audio_content: bytes, language: str = "pl") -> Dict[str, Any]:
        """Transcribe audio to text using Whisper"""
        if WhisperModel is None:
            return {
                "status": "error",
                "message": "Whisper not installed - install with: pip install faster-whisper"
            }
        
        if self.whisper_model is None:
            return {
                "status": "error", 
                "message": "Failed to load Whisper model"
            }
        
        # Create temp file for audio
        temp_file = None
        try:
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_content)
                temp_file_path = temp_file.name
            
            logger.info(f"Processing audio file: {temp_file_path}")
            
            # Transcribe with Whisper
            segments, info = self.whisper_model.transcribe(
                temp_file_path,
                language=language if language != "auto" else None,
                beam_size=5,
                word_timestamps=True
            )
            
            # Collect transcript with timestamps
            transcript_parts = []
            confidence_scores = []
            
            for segment in segments:
                transcript_parts.append(segment.text.strip())
                if hasattr(segment, 'avg_logprob'):
                    confidence_scores.append(segment.avg_logprob)
            
            # Combine transcript
            full_transcript = " ".join(transcript_parts).strip()
            
            # Calculate average confidence
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            logger.info(f"Transcription completed: '{full_transcript[:50]}...'")
            logger.info(f"Detected language: {info.language}")
            logger.info(f"Confidence: {avg_confidence:.2f}")
            
            return {
                "status": "ok",
                "transcript": full_transcript,
                "language": info.language,
                "confidence": avg_confidence,
                "duration": info.duration
            }
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return {
                "status": "error",
                "message": f"Transcription failed: {str(e)}"
            }
        finally:
            # Cleanup temp file
            if temp_file and os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    
    async def synthesize_speech(self, text: str, voice: str = "pl-PL-default") -> Dict[str, Any]:
        """Synthesize text to speech using Piper"""
        if piper is None or sf is None:
            return {
                "status": "warning",
                "voice": voice,
                "audio_url": "/static/audio/placeholder.wav",
                "message": "Piper TTS not installed - install with: pip install piper-tts soundfile"
            }
        
        if self.piper_model is None:
            return {
                "status": "warning", 
                "voice": voice,
                "audio_url": "/static/audio/placeholder.wav",
                "message": "Piper voice model not available - using placeholder"
            }
        
        try:
            logger.info(f"Starting speech synthesis for text: '{text[:50]}...'")
            
            # Generate unique filename
            audio_id = str(uuid.uuid4())
            audio_filename = f"speech_{audio_id}.wav"
            
            # Create static audio directory if not exists
            static_dir = Path("static/audio")
            static_dir.mkdir(parents=True, exist_ok=True)
            
            audio_path = static_dir / audio_filename
            
            # Synthesize speech using Piper
            import wave
            
            # Use synthesize_wav for direct file writing
            with wave.open(str(audio_path), 'w') as wav_file:
                self.piper_model.synthesize_wav(text, wav_file)
            
            sample_rate = self.piper_model.config.sample_rate
            
            # Get file info
            file_size = audio_path.stat().st_size
            # Estimate duration from file size (rough approximation)
            duration = file_size / (sample_rate * 2)  # 2 bytes per sample (16-bit)
            
            logger.info(f"Speech synthesis completed: {audio_filename}")
            logger.info(f"File size: {file_size} bytes")
            logger.info(f"Duration: {duration:.2f} seconds")
            
            return {
                "status": "ok",
                "voice": voice,
                "audio_url": f"/static/audio/{audio_filename}",
                "text_length": len(text),
                "audio_duration": duration,
                "file_size": file_size
            }
            
        except Exception as e:
            import traceback
            logger.error(f"Speech synthesis error: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "status": "error",
                "message": f"Speech synthesis failed: {str(e)}"
            }
