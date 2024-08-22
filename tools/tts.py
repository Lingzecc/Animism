import requests
from fish_speech_1_2.tools.api import start_fish_spich_api
def tts(text):
    url = "http://127.0.0.1:8000/v1/invoke"
    data = {
        "text": text,
        "reference_text": "null",
        "reference_audio": "null",
        "max_new_tokens": 1024,
        "chunk_length": 100,
        "top_p": 0.7,
        "repetition_penalty": 1.2,
        "temperature": 0.7,
        "emotion": "happy",
        "format": "wav",
        "streaming": "false",
        "ref_json": "ref_data.json",
        "ref_base": "ref_data",
        "speaker": "null"
    }

    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        audio_content = response.content

        with open("../data/tts_output/generated_audio.wav", "wb") as audio_file:
            audio_file.write(audio_content)
        print("Audio has been saved to 'generated_audio.wav'.")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.json())
start_fish_spich_api(url="http://127.0.0.1:8000")
tts("你好，我的名字叫灵泽，需要我的帮助吗？")
