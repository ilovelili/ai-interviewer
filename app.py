from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk
import wave

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI service credentials
speech_api_key = os.getenv("SPEECH_API_KEY")
region = os.getenv("REGION")
speech_endpoint = os.getenv("SPEECH_ENDPOINT")

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


def recognize_from_audio(file_path):
    try:
        # Creates an instance of a speech config with specified subscription key and service region.
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_api_key,
            region=region,
            speech_recognition_language="ja-JP",
        )

        # Creates a recognizer with the given settings
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

        # Create an audio configuration from the audio file
        audio_input = speechsdk.AudioConfig(filename=file_path)

        # Creates a recognizer with the given settings
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_input
        )

        # Starts speech recognition, and returns after a single utterance is recognized.
        result = speech_recognizer.recognize_once()

        # Check the result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
    except Exception as e:
        print(f"An error occurred: {e}")

    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    file_path = os.path.join("uploads", audio_file.filename)
    audio_file.save(file_path)

    recognized_text = recognize_from_audio(file_path)
    if recognized_text:
        return jsonify({"transcription": recognized_text})
    else:
        return jsonify({"error": "Speech recognition failed"}), 500


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
