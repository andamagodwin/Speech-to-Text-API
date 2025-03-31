from flask import Blueprint, request, jsonify, Response
from .speech_client import start_transcription_process
import json

bp = Blueprint('routes', __name__)

@bp.route('/transcribe', methods=['POST'])
def start_transcription():
    """Start a real-time transcription session."""
    language_code = request.args.get('language', 'en-US')
    return Response(
        start_transcription_process(language_code),
        mimetype='text/event-stream'
    )

@bp.route('/transcriptions', methods=['GET'])
def get_transcriptions():
    return jsonify({'transcriptions': []})