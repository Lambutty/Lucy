from flask import Flask, jsonify, request
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from queue import Queue
import threading
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

app = Flask(__name__)
auth = HTTPBasicAuth()

CORS(app)

# Set your desired username and password
USERNAME = 'admin'
PASSWORD = 'password'

model = Model(lang="de")
input_queue = Queue()

def callback(in_data, frame_count, time_info, status):
    input_queue.put(in_data)
    return (b'', pyaudio.paContinue)

def process_audio():
    recognizer = KaldiRecognizer(model, 16000)
    while True:
        data = input_queue.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print(result['text'])  # You can replace this with any action you want

@auth.verify_password
def verify_password(username, password):
    print(username, password)
    return username == USERNAME and password == PASSWORD

@app.route('/start-listening', methods=['GET'])
@auth.login_required
def start_listening():
    # Start a separate thread to process the audio
    global audio_thread
    audio_thread = threading.Thread(target=process_audio)
    audio_thread.start()

    # Start listening to the microphone
    p = pyaudio.PyAudio()
    global stream
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024, stream_callback=callback)
    stream.start_stream()

    return jsonify({'status': 'Listening started'})

@app.route('/stop-listening', methods=['GET'])
@auth.login_required
def stop_listening():
    # Stop listening and close the microphone stream
    stream.stop_stream()
    stream.close()
    
    # Clear the input queue and stop the audio processing thread
    input_queue.queue.clear()
    audio_thread.join()

    return jsonify({'status': 'Listening stopped'})

if __name__ == '__main__':
    app.run(debug=True)
