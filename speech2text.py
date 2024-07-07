import os
import azure.cognitiveservices.speech as speechsdk
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI service credentials
speech_endpoint = os.getenv("SPEECH_ENDPOINT")
speech_api_key = os.getenv("SPEECH_API_KEY")
speech_deployment_id = os.getenv("SPEECH_DEPLOYMENT_ID")

region = os.getenv("REGION")
subscription = os.getenv("SUBSCRIPTION_ID")

# https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_sample.py


def recognize_from_microphone():
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(
        subscription=subscription, region=region, speech_recognition_language="ja-JP", source_language_config="ja-JP"
    )

    config_str = f"Subscription Key: {subscription}, Region: {region}"

    print(config_str)

    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Say something...")

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. The task returns the recognition text as result.
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


def transcribe_text(text):
    url = f"{speech_endpoint}/openai/deployments/{speech_deployment_id}/transcriptions"

    headers = {"Content-Type": "application/json", "api-key": speech_api_key}

    payload = {"prompt": text, "model": "whisper"}

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()["transcription"]
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None


if __name__ == "__main__":
    recognized_text = recognize_from_microphone()
    if recognized_text:
        transcription = transcribe_text(recognized_text)
        if transcription:
            print("Transcription: ", transcription)
