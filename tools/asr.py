import os  # 导入os模块，提供与操作系统交互的功能。
import soundfile  # 导入soundfile模块，用于简化声音文件的读写操作。
from funasr import AutoModel  # 从funasr模块导入AutoModel类，funasr不是标准库，可能是自定义或特定库。
model = AutoModel(model="paraformer-zh-streaming", model_revision="v2.0.4", disable_update=True)  # 初始化语音识别模型。
chunk_size = [0, 10, 5]  # 定义录音块大小参数，这里表示600ms的录音块。
encoder_chunk_look_back = 4  # 定义编码器自注意力的回看录音块数。
decoder_chunk_look_back = 1  # 定义解码器交叉注意力的回看编码器录音块数。

audio_folder_path = 'data/record_audio/'  # 定义音频文件保存的文件夹路径。
audio_file_name = 'recorded_audio.wav'  # 定义音频文件的名称。
audio_file_path = os.path.join(audio_folder_path, audio_file_name)  # 拼接完整的音频文件路径。

def recognize_speech(wav_file=audio_file_path, model=model, chunk_size=chunk_size,
                     encoder_chunk_look_back=encoder_chunk_look_back, 
                     decoder_chunk_look_back=decoder_chunk_look_back):
    # 定义recognize_speech函数，用于使用语音识别模型处理音频文件。
    # 读取WAV文件，获取音频数据和采样率。
    speech, sample_rate = soundfile.read(wav_file)
    chunk_stride = chunk_size[1] * 960  # 计算每个录音块的步长。

    cache = {}  # 创建空字典，用于存储识别过程中的缓存数据。
    total_chunk_num = int(len(speech) / chunk_stride)  # 计算总的录音块数量。
    for i in range(total_chunk_num):  # 遍历每个录音块。
        speech_chunk = speech[i * chunk_stride:(i + 1) * chunk_stride]  # 获取当前录音块的数据。
        is_final = i == total_chunk_num - 1  # 判断是否是最后一个录音块。
        # 使用模型进行识别，并打印识别结果。
        res = model.generate(input=speech_chunk, cache=cache, is_final=is_final,
                            chunk_size=chunk_size, encoder_chunk_look_back=encoder_chunk_look_back,
                            decoder_chunk_look_back=decoder_chunk_look_back)
        return str(res)
    
print(recognize_speech())