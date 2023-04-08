# VoiceGPT

 - This is a basic python program which recognizes user's voice and computes it with the AI to get the response. The response is converted to speech and then played back to the user!
 - It has 2 different models, one is based on [EdgeGPT](https://github.com/acheong08/EdgeGPT) and the other is based on [LLaMa.cpp](https://github.com/ggerganov/llama.cpp)
 - EdgeGPT uses browser cookies and gets the response from the cloud where Bing's new chat feature is released. LLaMa on the other hand gets the response from the local API running on the user's computer.
 - The speed of everything here depends upon your PC specs. As the Voice recognition uses OpenAI's [Tiny Whisper Model](https://github.com/openai/whisper) that will be running on your PC to get the voice data.
 - Both GPUs and CPUs are supported, However GPUs are preferred more due to their speed. CPUs can work too but they will be kind of slower compared to GPU computing.
 - The Project is fully customisable! as it has a config file which has all the settings necessary to run the project on your local computer.

