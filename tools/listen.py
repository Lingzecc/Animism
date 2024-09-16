#一个录入一个识别
import pyaudio  # 导入pyaudio模块，用于音频输入输出操作。
import wave  # 导入wave模块，用于处理WAV格式音频文件。
import os  # 导入os模块，提供与操作系统交互的功能。
import soundfile  # 导入soundfile模块，用于简化声音文件的读写操作。
from funasr import AutoModel  # 从funasr模块导入AutoModel类，funasr不是标准库，可能是自定义或特定库。
import pyaudio, wave  # 导入所需的库
import numpy as np    # 导入numpy库，用于数据处理

import os  # 导入os模块
import re  # 导入正则表达式模块
import time


def listen():  # 定义listen函数，用于录音
    temp = 20  # 初始化一个变量temp，但实际未用到
    CHUNK = 1024  # 定义每次读取的音频数据块大小为1024字节
    FORMAT = pyaudio.paInt16  # 音频数据格式，16位整数PCM
    CHANNELS = 1  # 声道数，这里是单声道
    RATE = 16000  # 采样率，16000Hz
    RECORD_SECONDS = 2  # 录音时长，2秒
    WAVE_OUTPUT_FILENAME = 'recorded_audio.wav'  # 定义输出的wav文件名
    # 确保保存文件的目录存在
    directory = 'data/record_audio'
    if not os.path.exists(directory):
        os.makedirs(directory)  # 如果目录不存在，则创建它

    WAVE_OUTPUT_FILENAME = os.path.join(directory, 'recorded_audio.wav')  # 使用os.path.join确保路径正确

    mindb = 1500  # 设置录音的阈值，声音强度大于2000开始录音
    delayTime = 1.3  # 设置声音强度降低后的延迟时间，1.3秒
    p = pyaudio.PyAudio()  # 创建PyAudio实例
    stream = p.open(format=FORMAT,  # 打开音频流
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,  # 表示输入流
                    frames_per_buffer=CHUNK)  # 每次读取的数据块大小
    #print("开始!计时")  # 打印开始计时信息

    frames = []  # 初始化一个列表，用于存储音频帧
    flag = False  # 初始化一个标志位，用于判断是否开始录音
    stat = True  # 初始化一个标志位，用于判断是否继续录音
    stat2 = False  # 初始化一个标志位，用于判断声音是否变小

    tempnum = 0  # 初始化一个计时器变量
    tempnum2 = 0  # 初始化一个计时器变量，用于记录声音变小的时间点

    while stat:  # 当stat为True时，循环继续
        data = stream.read(CHUNK, exception_on_overflow=False)  # 读取音频数据
        frames.append(data)  # 将读取的数据添加到frames列表
        audio_data = np.frombuffer(data, dtype=np.short)  # 将数据转换为numpy数组
        temp = np.max(audio_data)  # 计算音频数据的最大值

        # 判断声音强度是否大于阈值，并开始录音
        if temp > mindb and flag == False:
            flag = True
            print("声音强度大于阈值")
            print("开始录音")
            tempnum2 = tempnum

        if flag:  # 如果已经开始录音
            # 如果声音强度小于阈值，并且之前没有记录声音变小的时间点
            if temp < mindb and stat2 == False:
                stat2 = True
                tempnum2 = tempnum
                #print("声音小，且之前是大的或刚开始，记录当前点")
            # 如果声音强度大于阈值，则重置声音变小的标志位
            if temp > mindb:
                stat2 = False
                tempnum2 = tempnum

            # 如果从声音变小开始已经过了delayTime秒，并且声音仍然小，则停止录音
            if (tempnum > tempnum2 + delayTime * 15) and stat2 == True:
                #print("间隔%.2lfs后开始检测是否还是小声" % delayTime)
                if (stat2 and temp < mindb):
                    stat = False
                    #print("小声！")
                else:
                    stat2 = False
                    #print("大声！")

        #print(str(temp) + "      " + str(tempnum))  # 打印当前声音强度和计时器
        tempnum = tempnum + 1  # 更新计时器
        # 如果计时器超过150（约12.5秒），则强制停止录音
        if tempnum > 150:
            stat = False

    #print("录音结束")  # 打印录音结束信息

    stream.stop_stream()  # 停止音频流
    stream.close()  # 关闭音频流
    p.terminate()  # 终止PyAudio实例

    # 将录制的音频数据写入wav文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)  # 设置声道数
    wf.setsampwidth(p.get_sample_size(FORMAT))  # 设置采样宽度
    wf.setframerate(RATE)  # 设置采样率
    wf.writeframes(b''.join(frames))  # 写入音频帧
    wf.close()  # 关闭wav文件

def recognize_speech(wav_file, model, chunk_size, encoder_chunk_look_back, decoder_chunk_look_back):
    # 读取WAV文件，获取音频数据和采样率。
    speech, sample_rate = soundfile.read(wav_file)
    chunk_stride = chunk_size[1] * 960  # 计算每个录音块的步长。

    cache = {}  # 创建空字典，用于存储识别过程中的缓存数据。
    total_chunk_num = int(len(speech) / chunk_stride)  # 计算总的录音块数量。
    recognized_texts = []  # 初始化一个列表来累积所有识别的文本。

    for i in range(total_chunk_num):  # 遍历每个录音块。
        speech_chunk = speech[i * chunk_stride:(i + 1) * chunk_stride]  # 获取当前录音块的数据。
        is_final = i == total_chunk_num - 1  # 判断是否是最后一个录音块。
        # 使用模型进行识别。
        res = model.generate(input=speech_chunk, cache=cache, is_final=is_final,
                             chunk_size=chunk_size, encoder_chunk_look_back=encoder_chunk_look_back,
                             decoder_chunk_look_back=decoder_chunk_look_back,
                             disable_pbar=True )
        # 假设res是一个列表，其中包含字典，每个字典都有'text'键
        for item in res:
            if 'text' in item:  # 检查字典中是否有'text'键
                recognized_texts.append(item['text'])  # 添加文本到列表

    # 将累积的识别文本连接成一行，并去除所有空格
    recognized_text = ''.join(recognized_texts)  # 直接连接文本，不添加空格
    recognized_text = recognized_text.replace(" ", "")  # 替换掉所有空格
    print("Recognized text:", recognized_text)
    return recognized_text  # 返回处理后的识别文本。




#disable_pbar=True 禁止状态信息被打印出来


def listen_and_recognize(model, chunk_size, encoder_chunk_look_back, decoder_chunk_look_back):
    audio_folder_path = 'data/record_audio/'
    audio_file_name = 'recorded_audio.wav'
    audio_file_path = os.path.join(audio_folder_path, audio_file_name)

    # 录音和识别的循环
    while True:
        # 这里应该调用实际的录音函数，录音一定时间或直到检测到声音结束
        # 假设 listen 函数录音后保存到 audio_file_path 指定的文件
        listen()  # 调用 listen 函数进行录音，这里需要你实现 listen 函数

        # 调用 recognize_speech 函数进行语音识别
        recognize_speech(audio_file_path, model, chunk_size, encoder_chunk_look_back, decoder_chunk_look_back)

        # 可以在这里添加休息时间，避免CPU过载
        time.sleep(1)  # 休息1秒


# def main():
#     # main函数是程序的入口点。
#     model = AutoModel(model="paraformer-zh-streaming", model_revision="v2.0.4")  # 初始化语音识别模型。
#     chunk_size = [0, 10, 5]  # 定义录音块大小参数。
#     encoder_chunk_look_back = 4  # 定义编码器自注意力的回看录音块数。
#     decoder_chunk_look_back = 1  # 定义解码器交叉注意力的回看编码器录音块数。

#     # 调用 listen_and_recognize 函数进行持续录音和识别
#     listen_and_recognize(model, chunk_size, encoder_chunk_look_back, decoder_chunk_look_back)


# if __name__ == "__main__":
#     main()  # 程序入口，调用main函数。