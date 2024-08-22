from flask import Flask, send_from_directory, request, flash, redirect
from pydub import AudioSegment 
import os
import json
app = Flask(__name__, static_folder='./')


 
# 音频转格式
def convert_audio_to_wav(input_audio_path, output_wav_path):  
    """  
    将音频文件转换为WAV格式。  
      
    参数:  
    - input_audio_path: 输入音频文件的路径（可以是MP3、OGG等格式）  
    - output_wav_path: 转换后WAV文件的保存路径  
    """  
    try:  
        # 加载音频文件  
        audio = AudioSegment.from_file(input_audio_path)  
          
        # 转换为WAV格式并保存  
        audio.export(output_wav_path, format="wav")  
        print(f"音频已成功转换为WAV格式，并保存到：{output_wav_path}")  
    except Exception as e:  
        print(f"转换失败：{e}") 

# 网页投射
@app.route('/')
def index():
    return app.send_static_file('./live2d.html')
# 投射皮套文件夹
@app.route('/assets/<path:path>')
def serve_static(path):
    return send_from_directory('./assets/',path)
  
# 音频位置
UPLOAD_FOLDER = 'data/record_audio/'  
if not os.path.exists(UPLOAD_FOLDER):  
    os.makedirs(UPLOAD_FOLDER)  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER    
# 保存录音
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
        file.save(filepath)
        convert_audio_to_wav(filepath,"data/record_audio/recorded_audio.wav")  
        return '文件上传成功'  


@app.route('/api/get_mouth_y')
def api_get_one_account():
    with open("tmp.txt", "r") as f:
        return json.dumps({
            "y": f.read()
        })
        

if __name__ == '__main__':
    app.run(port=4800, debug=True, host="0.0.0.0")