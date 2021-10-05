# Text to Speech imports
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

# Speech to Text imports
import azure.cognitiveservices.speech as speechsdk

speech_config_tts = SpeechConfig(subscription="f4c4b77403fc4b3a98706ea74a84708c", region="eastus")

# Write audio to file
audio_config = AudioOutputConfig(filename="./file.wav")

synthesizer = SpeechSynthesizer(speech_config=speech_config_tts, audio_config=audio_config)
synthesizer.speak_text_async("phuck.")

# Output audio on run
# audio_config = AudioOutputConfig(use_default_speaker=True)

# Store audio in mem as stream
# synthesizer = SpeechSynthesizer(speech_config=speech_config_tts, audio_config=None)
# result = synthesizer.speak_text_async("Getting the response as an in-memory stream.").get()
# stream = AudioDataStream(result)

# Store audio as stream and save to file
# speech_config_tts.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff24Khz16BitMonoPcm"])
# synthesizer = SpeechSynthesizer(speech_config=speech_config_tts, audio_config=None)

# result = synthesizer.speak_text_async("Customizing audio output format.").get()
# stream = AudioDataStream(result)
# stream.save_to_wav_file("./file.wav")

# Change audio output characteristics
# synthesizer = SpeechSynthesizer(speech_config=speech_config_tts, audio_config=None)

# ssml_string = open("ssml.xml", "r").read()
# result = synthesizer.speak_ssml_async(ssml_string).get()

# stream = AudioDataStream(result)
# stream.save_to_wav_file("./file.wav")



# Speech to Text from mic
# def from_mic():
#     speech_config_stt = speechsdk.SpeechConfig(subscription="f4c4b77403fc4b3a98706ea74a84708c", region="eastus")

#     # Specify different input device
#     # audio_config = AudioConfig(device_name="<device id>")
#     # speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config_stt, audio_config=audio_config)

#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config_stt)
    
#     print("Speak into your microphone.")
#     result = speech_recognizer.recognize_once_async().get()
#     print(result.text)

# from_mic()

def from_file():
    speech_config_stt = speechsdk.SpeechConfig(subscription="f4c4b77403fc4b3a98706ea74a84708c", region="eastus")
    audio_input = speechsdk.AudioConfig(filename="./file.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config_stt, audio_config=audio_input)
    
    result = speech_recognizer.recognize_once_async().get()
    print(result.text)

from_file()


# TODO: Figure out how to set the `profanityOption` to Raw


