from flask import Flask, send_from_directory, request, flash, redirect, send_file, jsonify
import os
import json
import moviepy.video.io.ffmpeg_tools
# from llm import chat
from tools.listen import recognize_speech
from tools.tts import tts
import pygame
import time
import numpy as np
import librosa
app = Flask(__name__)

# 网页投射
@app.route('/')
def web():
    return send_file('./live2d.html')



# 将皮套传输到路由
@app.route('/assets/<path:path>')
def live2d(path):
    return send_from_directory('./assets/',path)



# 音频位置
UPLOAD_FOLDER = 'data/record_audio/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 获取前端音频保存到UPLOAD_FOLDER
@app.route('/upload/audio', methods=['POST'])
def record_audio2wav():
    if 'audioFormData' not in request.files:
        flash('没有文件部分')
        return redirect(request.url)
    file = request.files['audioFormData']
    if file.filename == '':
        flash('没有选择文件')
        return redirect(request.url)
    if file:
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        towavfilepath = os.path.join(app.config['UPLOAD_FOLDER'], "recorded_audio.wav")
        file.save(filepath)
        # 转wav
        moviepy.video.io.ffmpeg_tools.ffmpeg_extract_audio(filepath, towavfilepath)
        print(f"音频已成功转换为WAV格式，并保存到{filepath}")
        return '文件上传成功'

response_llm = ""

@app.route('/upload/tts', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    # response_llm = chat(text)
    # tts(response_llm, "127.0.0.1", "8000", tmp_audio_path='data/tts_output')
    return send_file("D:/PORJECT/Animism/Allium/data/tts_output/tmp.wav", mimetype='audio/wav')
    


# 开口大小文件路由
"""
引用自https://juejin.cn/post/7242279345136861241
"""
@app.route('/api/mouth', methods=['GET'])
def mouth():
    with open("data/tts_output/tmp.txt", "r") as f:
        return json.dumps({
            "y": f.read()
        })  


       
@app.route('/mouthY', methods=['POST'])  
def mouthY(tmp_audio_path='data/tts_output'):
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




# @app.route('/data/asr')
# def test():
    
if __name__ == '__main__':
    app.run(port=4800, debug=True, host="0.0.0.0")