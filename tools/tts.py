import requests
from pathlib import Path
import pyaudio
import requests
import base64
import librosa
import time
import pygame
import numpy as np
# 使用前先运行api启动fish-speech(tools\fish_speech_1_2\tools\api.py)
host = "127.0.0.1"
port = "8000"

def wav_to_base64(file_path):
    if not file_path or not Path(file_path).exists():
        return None
    with open(file_path, "rb") as wav_file:
        wav_content = wav_file.read()
        base64_encoded = base64.b64encode(wav_content)
        return base64_encoded.decode("utf-8")


def read_ref_text(ref_text):
    path = Path(ref_text)
    if path.exists() and path.is_file():
        with path.open("r", encoding="utf-8") as file:
            return file.read()
    return ref_text


base64_audio = wav_to_base64(None)

ref_text = None
if ref_text:
    ref_text = read_ref_text(ref_text)
# 开启fish-speech的api后访问api转换返回语音
def tts(text, host, port, tmp_audio_path='data/tts_output'):
    url = f"http://{host}:{port}/v1/invoke"
    data = {
        "text": text,
        "reference_text": ref_text,
        "reference_audio": base64_audio,
        "max_new_tokens": 1024,
        "chunk_length": 100,
        "top_p": 0.7,
        "repetition_penalty": 1.2,
        "temperature": 0.7,
        "speaker": None,
        "emotion": "happy",
        "format": "wav",
        "streaming": "False",
    }

    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        audio_content = response.content

        with open(f"{tmp_audio_path}/tmp.wav", "wb") as audio_file:
            audio_file.write(audio_content)
        print("Audio has been saved to 'tmp.wav'.")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.json())
        
# 根据语音音频转数字写入文本,通过ajax异步检测文本变化实现口型实时操作
"""
引用自https://juejin.cn/post/7242279345136861241
"""
def tts_and_play_audio(tmp_audio_path='data/tts_output'):
    pygame.mixer.init()
    pygame.mixer.music.load(f"{tmp_audio_path}/tmp.wav")  
    pygame.mixer.music.set_volume(0.8) 

    x , sr = librosa.load(f"{tmp_audio_path}/tmp.wav", sr=8000)

    x = x  - min(x)
    x = x  / max(x)
    x= np.log(x) + 1
    x = x  / max(x) * 1.5

    # pygame.mixer.music.play()
    s_time = time.time()
    try:
        for _ in range(int(len(x) / 800)):
            it = x[int((time.time() - s_time) * 8000)+1]
            # print(it)
            if it < 0:
                it = 0
            with open(f"{tmp_audio_path}/tmp.txt", "w") as f:
                f.write(str(float(it)))
            time.sleep(0.1)
    except:
        pass

    time.sleep(0.1)
    with open(f"{tmp_audio_path}/tmp.txt", "w") as f:
        f.write("0")
# while True:
#     tts_and_play_audio(text="")
# tts_and_play_audio(text="")