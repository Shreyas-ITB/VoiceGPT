import asyncio
import re
import os
import whisper
from gtts import gTTS
import pydub
from pydub import playback
import speech_recognition as sr
from EdgeGPT import Chatbot, ConversationStyle
from threading import Thread
import platform
import configparser
import requests
from time import sleep
import signal
import sys

# Create a recognizer object and wake word variables
recognizer = sr.Recognizer()
config = configparser.ConfigParser()
lang = "en"
global bot_response
global newb_response
BING_WAKE_WORD = "bing"
LLAMA_WAKE_WORD = "lama"

if platform.system() == "Windows" or platform.system() == "win32" or platform.system() == "Win32":
    params = "config\\config.ini"
elif platform.system() == "linux2":
    params = "config/config.ini"
elif platform.system() == "darwin":
    params = "config/config.ini"

if platform.system() == "Windows" or platform.system() == "win32" or platform.system() == "Win32":
    cookie = "config\\cookies.json"
elif platform.system() == "linux2":
    cookie = "config/cookies.json"
elif platform.system() == "darwin":
    cookie = "config/cookies.json"

if platform.system() == "Windows" or platform.system() == "win32" or platform.system() == "Win32":
    modelpath = "models\\"
elif platform.system() == "linux2":
    modelpath = "models/"
elif platform.system() == "darwin":
    modelpath = "models/"

if platform.system() == "Windows" or platform.system() == "win32" or platform.system() == "Win32":
    audpath = "config\\audio.wav"
elif platform.system() == "linux2":
    audpath = "config/audio.wav"
elif platform.system() == "darwin":
    audpath = "config/audio.wav"

if platform.system() == "Windows" or platform.system() == "win32" or platform.system() == "Win32":
    respath = "config\\response.mp3"
elif platform.system() == "linux2":
    respath = "config/response.mp3"
elif platform.system() == "darwin":
    respath = "config/response.mp3"

if platform.system() == "Windows" or platform.system() == "win32" or platform.system() == "Win32":
    audppath = "config\\audio_prompt.wav"
elif platform.system() == "linux2":
    audppath = "config/audio_prompt.wav"
elif platform.system() == "darwin":
    audppath = "config/audio_prompt.wav"

def get_wake_word(phrase):
    if BING_WAKE_WORD in phrase.lower():
        return BING_WAKE_WORD
    elif LLAMA_WAKE_WORD in phrase.lower():
        return LLAMA_WAKE_WORD
    else:
        return None
    
def synthesize_speech(text, output_filename):
    response = gTTS(text=text, lang=lang, slow=False, tld="us")
    response.save(output_filename) 

def play_audio(file):
    sound = pydub.AudioSegment.from_file(file, format="mp3")
    playback.play(sound)

def get_params():
    config.read(params)
    port = config["Default"]["APIPort"]
    model = config["Default"]["ModelFilename"]
    resptime = config["Default"]["ResponseWaitTime"]
    LLaMainit = config["Default"]["LLaMainit"]
    return model, port, resptime, LLaMainit

def get_inputmode():
    config.read(params)
    InputMode = config["Default"]["Inputmode"]
    return InputMode

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def call_chat():
    model, port = get_params()
    if platform.system() == "Windows" or platform.system() == "win32" or platform.system() == "Win32":
        os.system(f"chat.exe -m ./{modelpath}{model} -H 127.0.0.1:{port}")
    elif platform.system() == "linux2":
        os.system(f"./chat.sh -m ./{modelpath}{model} -H 127.0.0.1:{port}")
    elif platform.system() == "darwin":
        os.system(f"./chat.sh -m ./{modelpath}{model} -H 127.0.0.1:{port}")

signal.signal(signal.SIGINT, signal_handler)

def call_API():
    if os.path.exists("chat") or os.path.exists("chat.exe"):
        newthr = Thread(target=call_chat)
        newthr.start()
    else:
        print("The Local AI files aren't compiled yet! Please compile them using (make) command or (cmake .) command in Windows.")
    return
    
async def main():
    modeln, portn, responsetime, LLaMainit = get_params()
    if LLaMainit.lower() == "yes":
        call_API()
    elif LLaMainit.lower() == "no":
        print("Could not initialise the LLaMa API, Specified value is set to no.. Continuing...")
    while True:
        InputMode = get_inputmode()
        if InputMode.lower() == "voice":
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print(f"Waiting for wake words, Saying GPT or Llama will wake me up...")
                while True:
                    audio = recognizer.listen(source)
                    try:
                        with open(audpath, "wb") as f:
                            f.write(audio.get_wav_data())
                        # Use the preloaded tiny_model
                        model = whisper.load_model("tiny")
                        result = model.transcribe(audpath)
                        phrase = result["text"]
                        print(f"You said: {phrase}")
                        wake_word = get_wake_word(phrase)
                        if wake_word is not None:
                            break
                        else:
                            print("Not a wake word. Try again.")
                    except Exception as e:
                        print("Error transcribing audio: {0}".format(e))
                        continue

                print("Speak a prompt...")
                synthesize_speech('What can I help you with?', respath)
                play_audio(respath)
                audio = recognizer.listen(source)

                try:
                    with open(audppath, "wb") as f:
                        f.write(audio.get_wav_data())
                    model = whisper.load_model("base")
                    result = model.transcribe(audppath)
                    user_input = result["text"]
                    print(f"You said: {user_input}")
                except Exception as e:
                    print("Error transcribing audio: {0}".format(e))
                    continue

                if wake_word == BING_WAKE_WORD:
                    bot = Chatbot(cookiePath=cookie)
                    response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.precise)

                    for message in response["item"]["messages"]:
                        if message["author"] == "bot":
                            bot_response = message["text"]

                    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)

                    bot = Chatbot(cookiePath=cookie)
                    response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.creative)
                    # Select only the bot response from the response dictionary
                    for message in response["item"]["messages"]:
                        if message["author"] == "bot":
                            bot_response = message["text"]
                    # Remove [^#^] citations in response
                    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
                    print("AI's response:", bot_response)
                    synthesize_speech(bot_response, 'response.mp3')
                    play_audio('response.mp3')
                else:
                    # Send prompt to llama model when called by the user
                    try:
                        if LLaMainit.lower() == "yes":
                            port = config["Default"]["APIPort"]
                            res = requests.post(f"http://127.0.0.1:{port}/prompt", user_input)
                            getid = res.text
                            print(getid)
                            resptime = config["Default"]["ResponseWaitTime"]
                            sleep(resptime)
                            getresp = requests.get(f"http://127.0.0.1:{port}/prompt/{getid}")
                            if getresp.status_code == 202:
                                print("Response from the model is still pending.. Please change the time in the config.ini...")
                            elif getresp.status_code == 404:
                                print("Error! Got invalid ID, can't retrive the response..")
                            else:
                                bot_response = getresp.json['response']
                            print("AI's response:", bot_response)
                            synthesize_speech(bot_response, 'response.mp3')
                            play_audio('response.mp3')
                        elif LLaMainit.lower() == "no":
                            print("Error! No response from the API. Are you sure the value in the config is set to 'yes'?")
                    except:
                        print("Error! Something went wrong..")
                    await bot.close()
        elif InputMode.lower() == "text":
            text_phrase = input("\033[1;32;40m> ")
            bot = Chatbot(cookiePath=cookie)
            response = await bot.ask(prompt=text_phrase, conversation_style=ConversationStyle.precise)

            for message in response["item"]["messages"]:
                if message["author"] == "bot":
                    newb_response = message["text"]
            
            newb_response = re.sub('\[\^\d+\^\]', '', newb_response)

            bot = Chatbot(cookiePath=cookie)
            response = await bot.ask(prompt=text_phrase, conversation_style=ConversationStyle.creative)
            # Select only the bot response from the response dictionary
            for message in response["item"]["messages"]:
                if message["author"] == "bot":
                    newb_response = message["text"]
            # Remove [^#^] citations in response
            newb_response = re.sub('\[\^\d+\^\]', '', newb_response)
            print("AI's response:", newb_response)
            await bot.close()
        else:
            print("Error!! The Inputmode in the config file should be either voice or text, Specified value not recognised..")
            return

if __name__ == "__main__":
    asyncio.run(main())