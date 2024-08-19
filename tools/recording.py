import pyaudio  # 导入pyaudio模块，用于音频输入输出操作。
import wave  # 导入wave模块，用于处理WAV格式音频文件。
def record_audio(filepath, duration):
    # 定义record_audio函数，用于录制音频。参数filepath是文件保存路径，duration是录音时长。
    p = pyaudio.PyAudio()  # 创建PyAudio实例。
    chunk = 256  # 定义每次读取的音频样本数。
    format = pyaudio.paInt16  # 定义音频数据格式为16位PCM。
    channels = 1  # 设置声道数为单声道。
    rate = 11025  # 设置采样率为11025Hz。

    # 打开音频流，准备录音。
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    print("开始录音：请在 {} 秒内输入语音".format(duration))  # 提示用户开始录音。
    frames = []  # 创建空列表，用于存储录音数据。

    # 循环读取音频数据，直到达到指定的录音时长。
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)  # 从音频流中读取chunk大小的数据。
        frames.append(data)  # 将读取的数据添加到frames列表中。

    print("录音结束")  # 打印录音结束提示。

    # 关闭音频流和PyAudio实例。
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存录音数据到WAV文件。
    wf = wave.open(filepath, 'wb')  # 打开filepath指定的文件用于写入。
    wf.setnchannels(channels)  # 设置文件声道数。
    wf.setsampwidth(p.get_sample_size(format))  # 设置样本宽度。
    wf.setframerate(rate)  # 设置文件采样率。
    wf.writeframes(b''.join(frames))  # 将frames列表中的音频数据写入文件。
    wf.close()  # 关闭文件。
    print("录音文件已保存：", filepath)  # 打印保存成功的提示。