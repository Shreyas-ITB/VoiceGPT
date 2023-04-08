# VoiceGPT

 - This is a basic python program which recognizes user's voice and computes it with the AI to get the response. The response is converted to speech and then played back to the user!
 - It has 2 different models, one is based on [EdgeGPT](https://github.com/acheong08/EdgeGPT) and the other is based on [LLaMa.cpp](https://github.com/ggerganov/llama.cpp)
 - EdgeGPT uses browser cookies and gets the response from the cloud where Bing's new chat feature is released. LLaMa on the other hand gets the response from the local API running on the user's computer.
 - The speed of everything here depends upon your PC specs. As the Voice recognition uses OpenAI's [Tiny Whisper Model](https://github.com/openai/whisper) that will be running on your PC to get the voice data.
 - Both GPUs and CPUs are supported, However GPUs are preferred more due to their speed. CPUs can work too but they will be kind of slower compared to GPU computing.
 - The Project is fully customisable! as it has a config file which has all the settings necessary to run the project on your local computer.
 - 
## Requirements

- You need Python 3.9 as Pytorch doesn't support the latest versions.
- You need a good PC to run the models. Mid range hardware with minimal processor will also work.
- You should have access to Bing Chat.
- Microsoft Bing browser to get the cookies.

## Installation

First you need to clone the repository using git clone. \
`git clone https://github.com/Shreyas-ITB/VoiceGPT` \
Or just download the latest release from the [releases page]() 

Now you need cookies from your Microsoft Edge browser. To get that open your Edge browser and install this extension.
- [for chrome or chromium based browsers](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
- [for firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Go to `bing.com` on your microsoft browser
- Open the extension
- Click "Export" on the bottom right, then "Export as JSON" (This saves your cookies to clipboard)
- Go to the config directory, open the cookies.json file and paste your cookie data.

In the terminal or CMD enter the below command to install the project module requirements. \
`pip install -r ./config/requirements.txt` \
or on windows \
`pip install -r .\config\requirements.txt`

Now you need to configure the config.ini file as per your prefrence.
- The config.ini file is located in the config directory.
```
[Default]
# Leave this default if your model file name is the same.
# Enter your model file name in the below field.

ModelFilename = ggml-model-q4_1.bin

# Leave this default if you don't want a different port.
# Enter a different port number in which the API will be hosted.

APIPort = 8080

# Enter the API Response call wait time in seconds here.
# This let's the API know when to get back the response, This also depends on your system RAM.
# If you have more RAM then probably it will be 5 seconds, less RAM then higher than 5 seconds.

ResponseWaitTime = 5

# If you want to run LLaMa on your local machine then specify the below field as yes.
# If you only want EdgeGPT then you can leave it as it is or just specify the below field as no.

LLaMainit = no

# If you don't want Voice input to the AI (controlled by voice) then you can leave it as it is.
# However if you want the Voice input then change the below setting to voice instead of text.
# Voice will activate the AI using your voice. Text will allow you to type the prompt!

Inputmode = text
```

