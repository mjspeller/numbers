from flask import Flask, render_template, jsonify, send_from_directory
import random
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    app.run(host='0.0.0.0', port=5000, debug=True)
