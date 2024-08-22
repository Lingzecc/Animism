from pydub import AudioSegment 

# 音频转格式
def convert_audio_to_wav():  
    """  
    将音频文件转换为WAV格式。  
      
    参数:  
    - input_audio_path: 输入音频文件的路径（可以是MP3、OGG等格式）  
    - output_wav_path: 转换后WAV文件的保存路径  
    """  
    try:  
        AudioSegment.converter = "D:\下载\GPT-SoVITS-beta0217\GPT-SoVITS-beta0217\\ffmpeg.exe"
        AudioSegment.ffmpeg = "D:\下载\GPT-SoVITS-beta0217\GPT-SoVITS-beta0217\\ffmpeg.exe"
        AudioSegment.ffprobe = "D:\下载\GPT-SoVITS-beta0217\GPT-SoVITS-beta0217\\ffprobe.exe"
        # 加载音频文件  
        audio = AudioSegment.from_wav("D:\PORJECT\Animism\Allium\hh.wav")  
          
        # 转换为WAV格式并保存  
        audio.export("D:/PORJECT/Animism/Allium/data/record_audio/recorded_audio.wav", format="wav")  
        print("音频已成功转换为WAV格式，并保存到")  
    except Exception as e:  
        print(f"转换失败：{e}") 
convert_audio_to_wav()
        
