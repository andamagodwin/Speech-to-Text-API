import queue
import re
import threading
from google.cloud import speech
import pyaudio
import json

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream:
    def __init__(self, rate=RATE, chunk=CHUNK):  # Make sure parameters are properly defined
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self.closed = True
        self.transcriptions = []
        self.current_interim = ""
def process_responses(responses: object, stream: MicrophoneStream) -> None:
    """Process server responses and store transcriptions."""
    # [Keep the entire process_responses function here]

def start_transcription_process(language_code: str):
    """Main transcription logic that yields results"""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    stream = MicrophoneStream(RATE, CHUNK)
    stream.__enter__()

    def generate():
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )
        responses = client.streaming_recognize(streaming_config, requests)
        
        threading.Thread(target=process_responses, args=(responses, stream)).start()
        
        try:
            while True:
                if stream.transcriptions:
                    yield f"data: {json.dumps({'final': stream.transcriptions.pop(0)})}\n\n"
                elif stream.current_interim:
                    yield f"data: {json.dumps({'interim': stream.current_interim})}\n\n"
        finally:
            stream.__exit__(None, None, None)

    return generate()