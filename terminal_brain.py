from tools.asr import recognize_speech
from tools.llm import chat
from tools.tts import tts_and_play_audio

def dialogue():
    query = recognize_speech()
    answer = chat(query=query)
    tts_and_play_audio(text=answer)

if __name__ == '__main__':
    dialogue()