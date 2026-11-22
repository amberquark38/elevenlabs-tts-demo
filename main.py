import os
import sys
import requests

API_BASE = 'https://api.elevenlabs.io/v1/text-to-speech'
DEFAULT_VOICE = '21m00Tcm4TlvDq8ikWAM'


def synthesize(text, voice_id=DEFAULT_VOICE, out_path='output.mp3'):
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        raise RuntimeError('Set ELEVENLABS_API_KEY first')
    url = f'{API_BASE}/{voice_id}'
    headers = {
        'xi-api-key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg'
    }
    payload = {
        'text': text,
        'model_id': 'eleven_multilingual_v2',
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75
        }
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f'API error {resp.status_code}: {resp.text[:200]}')
    with open(out_path, 'wb') as f:
        f.write(resp.content)
    return out_path


def main():
    text = ' '.join(sys.argv[1:]) or 'Hello from ElevenLabs text to speech demo.'
    path = synthesize(text)
    print(f'Audio saved to {path}')


if __name__ == '__main__':
    main()