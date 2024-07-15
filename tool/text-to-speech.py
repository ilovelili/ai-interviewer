from gtts import gTTS

# Japanese text to convert to speech
text = "こんにちは。これは日本語の音声サンプルです。"

# Generate speech
tts = gTTS(text, lang='ja')
tts.save("japanese_sample.mp3")

print("Japanese sample audio saved as japanese_sample.mp3")
