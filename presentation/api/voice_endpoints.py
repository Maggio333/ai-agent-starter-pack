"""
Voice API Endpoints - FastAPI routes for voice processing
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional, Dict, Any
import logging
import os

from infrastructure.services.voice_service import VoiceService
from application.container import Container

router = APIRouter()
logger = logging.getLogger(__name__)

def get_voice_service() -> VoiceService:
    """Dependency injection for voice service"""
    container = Container()
    return container.voice_service()


@router.post("/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = Form("pl"),
    voice_service: VoiceService = Depends(get_voice_service)
) -> Dict[str, Any]:
    """
    Transcribe audio file to text using Whisper
    """
    logger.info(f"Received audio file: {audio.filename}")
    logger.info(f"Content type: {audio.content_type}")
    logger.info(f"File size: {audio.size} bytes")
    
    try:
        # Read audio content
        audio_content = await audio.read()
        
        # Transcribe using voice service
        result = await voice_service.transcribe_audio(audio_content, language)
        
        return result
        
    except Exception as e:
        logger.error(f"Transcription endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/speak")
async def synthesize_speech(
    text: str = Form(...),
    voice: str = Form("pl-PL-default"),
    voice_service: VoiceService = Depends(get_voice_service)
) -> Dict[str, Any]:
    """
    Synthesize text to speech using Piper
    """
    logger.info(f"Received text for synthesis: '{text[:50]}...'")
    logger.info(f"Voice: {voice}")
    
    try:
        # Synthesize using voice service
        result = await voice_service.synthesize_speech(text, voice)
        
        return result
        
    except Exception as e:
        logger.error(f"Speech synthesis endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """
    Serve audio files from static directory
    """
    try:
        audio_path = f"static/audio/{filename}"
        
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        return FileResponse(audio_path, media_type="audio/wav")
        
    except Exception as e:
        logger.error(f"Audio file serving error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def voice_health_check(voice_service: VoiceService = Depends(get_voice_service)):
    """
    Health check for voice services
    """
    try:
        whisper_status = "available" if voice_service.whisper_model is not None else "unavailable"
        piper_status = "available" if voice_service.piper_model is not None else "unavailable"
        
        return {
            "status": "healthy",
            "services": {
                "whisper_stt": whisper_status,
                "piper_tts": piper_status
            },
            "message": "Voice services health check completed"
        }
        
    except Exception as e:
        logger.error(f"Voice health check error: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }