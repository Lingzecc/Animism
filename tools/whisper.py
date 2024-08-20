import os  # 导入os模块，提供与操作系统交互的功能。
import soundfile  # 导入soundfile模块，用于简化声音文件的读写操作。
from funasr import AutoModel  # 从funasr模块导入AutoModel类，funasr不是标准库，可能是自定义或特定库。
from recording import record_audio
def whisper():
    # main函数是程序的入口点。
    model = AutoModel(model="paraformer-zh-streaming", model_revision="v2.0.4")  # 初始化语音识别模型。

    audio_folder_path = '../data/asr_output/'  # 定义音频文件保存的文件夹路径。
    audio_file_name = 'test.wav'  # 定义音频文件的名称。
    audio_file_path = os.path.join(audio_folder_path, audio_file_name)  # 拼接完整的音频文件路径。
    user_input = input("是否开始录音？输入 '是' 开始录音，输入 '退出' 结束程序：")  # 提示用户输入。
    record_audio(audio_file_path, 5)  # 调用record_audio函数进行录音。
    text = 
