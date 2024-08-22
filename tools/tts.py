import requests
import librosa
import time
import pygame
import numpy as np
host = "127.0.0.1"
port = "8000"
def tts(text, host, port):
    url = f"http://{host}:{port}/v1/invoke"
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





def tts_and_play_audio(text):
    tmp_audio_path = '../data/tts_output/generated_audio.wav'
    tts(text, tmp_audio_path)
    pygame.mixer.init()
    pygame.mixer.music.load(tmp_audio_path)  
    pygame.mixer.music.set_volume(0.8) 

    x , sr = librosa.load(tmp_audio_path, sr=8000)

    x = x  - min(x)
    x = x  / max(x)
    x= np.log(x) + 1
    x = x  / max(x) * 1.2

    pygame.mixer.music.play()
    s_time = time.time()
    try:
        for _ in range(int(len(x) / 800)):
            it = x[int((time.time() - s_time) * 8000)+1]
            # print(it)
            if it < 0:
                it = 0
            with open("generated_audio.txt", "w") as f:
                f.write(str(float(it)))
            time.sleep(0.1)
    except:
        pass

    time.sleep(0.1)
    with open("generated_audio.txt", "w") as f:
        f.write("0")

