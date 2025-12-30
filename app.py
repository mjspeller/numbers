from flask import Flask, render_template, jsonify, send_from_directory, request, Response
import random
import os
import io

app = Flask(__name__)

# Optional Kokoro TTS - only load if model exists
kokoro_pipeline = None
AI_VOICE_PATH = '/app/ai_voice'

def init_kokoro():
    global kokoro_pipeline
    if os.path.exists(AI_VOICE_PATH) and os.listdir(AI_VOICE_PATH):
        try:
            from kokoro import KPipeline
            kokoro_pipeline = KPipeline(lang_code='a')
            print("Kokoro TTS loaded successfully!")
        except Exception as e:
            print(f"Kokoro TTS not available: {e}")
            kokoro_pipeline = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tts-available')
def tts_available():
    """Check if TTS is available"""
    return jsonify({'available': kokoro_pipeline is not None})

@app.route('/speak', methods=['POST'])
def speak():
    """Generate speech from text using Kokoro TTS"""
    if kokoro_pipeline is None:
        return jsonify({'error': 'TTS not available'}), 503
    
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        import soundfile as sf
        
        # Generate audio
        generator = kokoro_pipeline(text, voice='af_heart', speed=1.0)
        audio_data = None
        for gs, ps, audio in generator:
            audio_data = audio
            break  # Just get the first chunk
        
        if audio_data is None:
            return jsonify({'error': 'Failed to generate audio'}), 500
        
        # Convert to WAV
        buffer = io.BytesIO()
        sf.write(buffer, audio_data, 24000, format='WAV')
        buffer.seek(0)
        
        return Response(buffer.read(), mimetype='audio/wav')
    except Exception as e:
        print(f"TTS error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/random/<int:max_num>')
def get_random(max_num):
    return jsonify({'number': random.randint(0, max_num)})

@app.route('/random-media/<path:media_path>')
def get_random_media(media_path):
    base_path = f'/app/{media_path}'
    try:
        files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
        if files:
            return jsonify({'file': random.choice(files)})
    except:
        pass
    return jsonify({'file': None})

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('/app/images', filename)

@app.route('/sounds/<path:filename>')
def serve_sound(filename):
    return send_from_directory('/app/sounds', filename)

if __name__ == '__main__':
    init_kokoro()
    app.run(host='0.0.0.0', port=5000, debug=True)
