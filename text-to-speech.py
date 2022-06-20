import sys
import os
import codecs
import chardet 
import azure.cognitiveservices.speech as speechsdk
from pathlib import Path


def text_to_speech_azure(key, region, text, output):
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    languageCode = 'zh-CN'
    ssmlGender = 'FEMALE'
    voicName = 'zh-CN-XiaoxiaoNeural'
    speakingRate = '25%'
    pitch = '0%'
    voiceStyle = 'default'
    head1 = f'<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="{languageCode}">'
    head2 = f'<voice name="{voicName}">'
    head3 =f'<mstts:express-as style="{voiceStyle}">'
    head4 = f'<prosody rate="{speakingRate}" pitch="{pitch}">'
    tail= '</prosody></mstts:express-as></voice></speak>'

    ssml = head1 + head2 + head3 + head4 + text + tail
    # print('this is the ssml======================================')
    # print(ssml)
    # print('end ssml======================================')
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    # synthesizer.speak_text_async(text)
    synthesizer.speak_ssml_async(ssml)

def generate_mp3():
    out_dir = 'audio-out'
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    key = os.getenv('az_key', '')
    region = os.getenv('az_region', 'westus') 
    dir = os.getenv('dir', '')
    if dir not in os.environ:
        filename = os.getenv('filename', '')
        if len(filename) == 0:
            print('please export filename or dir')
            return
        dir = os.getcwd()+ "/"+ os.path.splitext(filename)[0]

    if(not key or not dir):
        print("Please export az_key and dir")    
        return

    for file in os.listdir(dir):
        if file.endswith(".txt"):
            filePath = os.path.join(dir, file)
            with open(filePath, 'r',encoding='utf-8') as file:
                filenumber = os.path.basename(filePath).split('.')[0]
                data = file.read()
                output = out_dir + '/' + os.path.basename(dir) + "_" + str(filenumber) + ".mp3"
                print('converting to audio to ' + os.path.basename(dir) + "_" + str(filenumber) + ".mp3")
                text_to_speech_azure(key, region, data, output)


generate_mp3()