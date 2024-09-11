from flask import Flask, send_from_directory, request, flash, redirect, send_file, jsonify
import os
import json
import moviepy.video.io.ffmpeg_tools
# from llm import chat
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
@app.route('/upload', methods=['POST'])
def record_audio2wav():
    if 'audioFile' not in request.files:
        flash('没有文件部分')
        return redirect(request.url)
    file = request.files['audioFile']
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



# 开口大小文件路由
"""
引用自https://juejin.cn/post/7242279345136861241
"""
@app.route('/api/mouth')
def mouth():
    with open("data/tts_output/tmp.txt", "r") as f:
        return json.dumps({
            "y": f.read()
        })  
        
        
        
@app.route('/data/tts', methods=['GET'])  
def get_audio_file():  
    # 添加一个查询参数来绕过缓存，这里使用当前时间戳  
    timestamp = request.args.get('timestamp', 0)  
    # 确保timestamp是一个整数
    timestamp = int(timestamp) if timestamp.isdigit() else 0  
    print(f"/data/tts?{timestamp}")
    # 返回音频文件  
    return send_from_directory("data/tts_output/", 'tmp.wav', as_attachment=True)


# @app.route('/data/llm', methods=['GET'])  
# def get_text():
#     text = chat()
#     return json.dumps({
#         "text": text
#     })



# @app.route('/data/asr')
# def test():
    
if __name__ == '__main__':
    app.run(port=4800, debug=True, host="0.0.0.0")