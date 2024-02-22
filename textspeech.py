from google.cloud import texttospeech
import time
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\A05\key\\original-glider-400308-7f0f9b7bcec1.json'
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play

#pip install pygame
#pip install simpleaudio

def TextToSpeech(text_to_speech):
    # Instantiate a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_to_speech)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="yue-HK", ssml_gender='FEMALE'
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("C:\\A05\\FYP-test\\sound\\output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    out.close()
def main():
    text_to_speech = "Hello world"
    TextToSpeech(text_to_speech)
    playsound('C:\\A05\\FYP-test\\sound\\output.mp3')

if __name__ == "__main__":
    main()