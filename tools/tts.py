import requests
from pathlib import Path
import requests
import base64
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
    # 本地访问
    # url = f"http://{host}:{port}/v1/invoke"
    # 远程访问
    url = url = "https://api.fish.audio/v1/tts"
    querystring = {"author_id":"1aacaeb1b840436391b835fd5513f4c4"}
    headers = {
    "Authorization": "Bearer f56f8b383e8a46e482e0213e942748ff",
    "Content-Type": "application/json"
}
    
    # data = {
    #     "text": text,
    #     "reference_text": ref_text,
    #     "reference_audio": base64_audio,
    #     "max_new_tokens": 1024,
    #     "chunk_length": 100,
    #     "top_p": 0.7,
    #     "repetition_penalty": 1.2,
    #     "temperature": 0.7,
    #     "speaker": None,
    #     "format": "wav",
    #     "streaming": "False",
    # }

    data = {
        "text": text,
        "reference_id": "1aacaeb1b840436391b835fd5513f4c4",
        "chunk_length": 200,
        "max_new_tokens": 1024,
        "normalize": True,
        "format": "wav",
        "mp3_bitrate": 64,
        "latency": "normal"
    }
    
    # response = requests.post(url, json=data)
    response = requests.request("POST", url, json=data, headers=headers)
    
    if response.status_code == 200:
        audio_content = response.content
        # audio_content = response.text

        with open(f"{tmp_audio_path}/tmp.wav", "wb") as audio_file:
            audio_file.write(audio_content)
        print("Audio has been saved to 'tmp.wav'.")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.json())