from flask import Flask, send_from_directory, request, flash, redirect, send_file
import os
import json
import moviepy.video.io.ffmpeg_tools
app = Flask(__name__, static_folder='./')

# 网页投射
@app.route('/')
def index():
    return app.send_static_file('./live2d.html')
# 将皮套传输到路由
@app.route('/assets/<path:path>')
def serve_static(path):
    return send_from_directory('./assets/',path)
  
# 音频位置
UPLOAD_FOLDER = 'data/record_audio/'  
if not os.path.exists(UPLOAD_FOLDER):  
    os.makedirs(UPLOAD_FOLDER)  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER    
# 获取前端音频保存到UPLOAD_FOLDER
@app.route('/upload', methods=['POST'])  
def upload_file():  
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
@app.route('/api/get_mouth_y')
def api_get_one_account():
    with open("data/tts_output/tmp.txt", "r") as f:
        return json.dumps({
            "y": f.read()
        })

@app.route('/audio/<filename>', methods=['GET'])  
def audio_file(filename):  
    # 假设音频文件存储在应用的static文件夹下的audio子文件夹中  
    return send_from_directory('./data/tts_output/', filename)

if __name__ == '__main__':
    app.run(port=4800, debug=True, host="0.0.0.0")