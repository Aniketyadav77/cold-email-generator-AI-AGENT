"""
Voice AI Agent - Audio Processing Utilities

This module provides enhanced audio validation and processing capabilities
for the Voice AI Agent application.
"""

import streamlit as st
from typing import Tuple, Optional
import os


def validate_audio_format(filename: str) -> bool:
    """Check if the audio file format is supported."""
    supported_formats = ['.wav', '.mp3', '.m4a', '.ogg', '.flac', '.aac']
    return any(filename.lower().endswith(fmt) for fmt in supported_formats)


def get_audio_file_info(audio_file) -> dict:
    """Extract information from uploaded audio file."""
    try:
        return {
            'name': getattr(audio_file, 'name', 'unknown'),
            'size': getattr(audio_file, 'size', 0),
            'type': getattr(audio_file, 'type', 'unknown')
        }
    except Exception:
        return {'name': 'unknown', 'size': 0, 'type': 'unknown'}


def process_voice_input(audio_file, transcript_text: str) -> dict:
    """Process voice input and return structured data for email generation."""
    result = {
        'has_audio': audio_file is not None,
        'has_transcript': bool(transcript_text.strip()),
        'content': transcript_text.strip(),
        'source': 'voice' if audio_file else 'text'
    }
    
    if audio_file:
        audio_info = get_audio_file_info(audio_file)
        result['audio_info'] = audio_info
        result['content'] = transcript_text or f"Voice input from {audio_info['name']}"
    
    return result


# Voice AI Agent configuration constants
VOICE_CONFIG = {
    'max_file_size_mb': 25,
    'supported_formats': ['wav', 'mp3', 'm4a', 'ogg', 'flac', 'aac'],
    'demo_responses': {
        'short': "Brief professional introduction with key skills mentioned",
        'medium': "Detailed experience overview with specific technologies and achievements",
        'long': "Comprehensive background including leadership, technical expertise, and career goals"
    }
}
