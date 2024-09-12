from tools.listen import  listen, recognize_speech
from llm import chat
import os
from tools.tts import tts_and_play_audio
from funasr import AutoModel
import time
from load_config import Load_Config
import torch
# main函数是程序的入口点。
model = AutoModel(model="paraformer-zh-streaming", model_revision="v2.0.4")  # 初始化语音识别模型。
chunk_size = [0, 10, 5]  # 定义录音块大小参数。
encoder_chunk_look_back = 4  # 定义编码器自注意力的回看录音块数。
decoder_chunk_look_back = 1  # 定义解码器交叉注意力的回看编码器录音块数。
audio_folder_path = 'data/record_audio/'
audio_file_name = 'recorded_audio.wav'
audio_file_path = os.path.join(audio_folder_path, audio_file_name)

# 初始化参数
cfg = Load_Config()
config = cfg.get_config()
model_name_or_path = config['model_name_or_path'] # 模型地址
model_cache_path = config['model_cache_path'] # 模型缓存地址
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") # 判断是否能使用gpu
print(device)
fine_weight = config["finetune_weight_path"] + "epoch_2" # 微调保存地址
template_path = config["template"] # 模板地址

# 读取模板内容
def get_template(template_path):
    with open(template_path, "r", encoding="UTF-8") as f:  # 打开文件
        system_template = f.read()
    return system_template

# 获取设定
system_message = get_template(template_path)

# 定义模板
template = [{"role": "system", "content": system_message}]
# 生成器参数
generate_config = {
        "max_new":300,
        "do_sample":True,
        "top_p":0.8,
        "top_k":5,
        "temperature": 0.3,
        "repetition_penalty":1.1,
        "system_message": system_message,
        "sys_token_id": 0,
        "user_token_id": 3,
        "bot_token_id": 4
    }


def ter(yourInput, use_asr):

    print("=====预设生成参数:", generate_config)
    if isinstance(yourInput, str):
        # 调用 recognize_speech 函数进行语音识别
        response_asr = yourInput
    else:
        response_asr = recognize_speech(yourInput, model, chunk_size, encoder_chunk_look_back, decoder_chunk_look_back)
    #添加休息时间，避免CPU过载
    time.sleep(1)  # 休息1秒
    response_llm = chat(response_asr, template)
    tts_and_play_audio(response_llm, tmp_audio_path='data/tts_output')
        